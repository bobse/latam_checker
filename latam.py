import itertools
import json
import time
from datetime import datetime, timedelta
from multiprocessing import Pool
from typing import List, Dict, Tuple

import requests


def _request_json(
    departure_date: datetime.date,
    return_date: datetime.date,
    origin_airport: str,
    dest_airport: str,
    num_attemps: int = 5,
) -> (Dict, float):
    """
    Retrieves json from Latam, returns a tuple a dict with all the flights and the best price

    """
    departure_date = departure_date.strftime("%Y-%m-%d")
    return_date = return_date.strftime("%Y-%m-%d")
    url = f"http://bff.latam.com/ws/proxy/booking-webapp-bff/v1/public/revenue"\
        f"/bestprices/roundtrip?departure={departure_date}&origin={origin_airport}"\
        f"&destination={dest_airport}&cabin=Y&country=BR&language=PT&home=pt_br"\
        f"&return={return_date}&adult=1&promoCode="

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    }

    for attempts in range(num_attemps):
        try:
            # print(f"{departure_date} -> {return_date}")
            page = requests.get(url, headers=headers, timeout=15)
            page.raise_for_status()

            if "application/json" in page.headers["content-type"]:
                response = json.loads(page.text)
                return _reformat_latam_json(response.get("bestPrices")), response.get(
                    "cheapestPrice"
                )
            else:
                raise requests.exceptions.InvalidJSONError

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as err:
            print(f"Error: {err}")
            print(f"Trying it again in {str(attempts * 2)} seconds")
            time.sleep(attempts * 2)
            continue

        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            print(f"Error: {e} | code: {code}")
            if code in [429, 500, 502, 503, 504]:
                # retry after n seconds
                time.sleep(attempts * 2)
                continue

        except Exception as e:
            print(f"Error: {e}")
            break

        return {}


def _reformat_latam_json(json_flights: List[Dict]) -> Dict:
    """
    Reformats latam response using departure date as key and a dict for return date with the
    date as key as well.
    ie: {'2022-09-28': {'2022-10-12': 1530.68, '2022-10-13': 2061.2}}
    """
    response = {}
    for dt_departure in json_flights:
        response[dt_departure["departureDate"]] = {}
        for dt_return in dt_departure["returnDates"]:
            if dt_return["available"]:
                response[dt_departure["departureDate"]].update(
                    {dt_return["date"]: dt_return["price"]["amount"]}
                )
            else:
                response[dt_departure["departureDate"]].update({dt_return["date"]: 0})
    return response


def _merge_responses(dict_array: List[Dict]) -> Dict:
    """
    Merges all the response dicts into a single one
    """
    response = {}
    for item in dict_array:
        for key in item.keys():
            if response.get(key):
                response[key].update(item[key])
            else:
                response[key] = item[key]
    return response


def get_all_dates(
    departure_date: str,
    origin_airport: str,
    dest_airport: str,
) -> tuple[Dict, float]:
    """
    Searches 21 days from the departure date and returns a matrix with all possible
    values/combinations

    """
    departure_date = datetime.strptime(departure_date, "%Y-%m-%d")
    all_dates = [departure_date + timedelta(days=7 * x) for x in range(0, 3)]
    trips = [i for i in itertools.combinations_with_replacement(all_dates, 2)]
    func_params = [
        (item[0], item[1], origin_airport, dest_airport) for item in trips
    ]
    with Pool(processes=16) as pool:
        results = pool.starmap(_request_json, func_params)
    best_price = results[0][1]
    list_of_responses = []
    for item in results:
        if item[1] < best_price:
            best_price = item[1]
        list_of_responses.append(item[0])

    return _merge_responses(list_of_responses), best_price


def convert_to_matrix(response_json: Dict) -> Tuple[Dict, List]:
    """
    Converts the response into a matrix for better implementation of the html table

    :param response_json: merged json return from the function merge_responses
    :return: tuple(dict:{idx:date}, list: a matrix of width = length with all possible
    combinations of dates)

    """
    # 0 position is index and 1 position is the date(key)
    array_map_dates = {i[0]: i[1] for i in enumerate(response_json.keys())}
    # setup an array with zeros
    final_array = [[0 for x in array_map_dates] for y in array_map_dates]
    # substitute the zeros for the actual values
    for x in array_map_dates.items():
        for y in array_map_dates.items():
            if response_json[x[1]].get(y[1]):
                final_array[x[0]][y[0]] = response_json[x[1]].get(y[1])

    return array_map_dates, final_array


if __name__ == "__main__":
    params = dict(
        departure_date="2022-10-15",
        origin_airport="CGH",
        dest_airport="VIX",
    )
    res, cheap = get_all_dates(**params)
    with open("./response.json", "+w") as file:
        json.dump(res, file, indent=6)

    map_idx, matrix = convert_to_matrix(res)
