from __future__ import annotations

import itertools
import json
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from logging.config import dictConfig
from multiprocessing import Pool

import requests

from settings import LogConfig


dictConfig(LogConfig().dict())
LOGGER = logging.getLogger("app.latam")


class TicketFinder(ABC):
    """
    Interface for ticket finder
    Must always define url when creating a subclass
    """
    number_of_total_searches = 3

    @abstractmethod
    def __init__(self, departure_date: str, origin: str, destination: str):
        self._save_departure_date(departure_date)
        self.origin = origin
        self.destination = destination
        self._generate_travel_dates()
        self.best_price = float('inf')
        self.all_flights = {}

    def _save_departure_date(self, departure_date: str) -> None:
        departure_date = self._convert_str_to_date(departure_date)
        if departure_date.date() < datetime.now().date():
            LOGGER.error("Invalid date in search. Date is smaller than current date.")
            raise ValueError("Date must be bigger than the current date")
        else:
            self.departure_date = departure_date

    @staticmethod
    def _convert_str_to_date(departure_date: str) -> datetime.date:
        return datetime.strptime(departure_date, "%Y-%m-%d")

    @abstractmethod
    def _generate_travel_dates(self) -> None:
        """
            Generates all possible travel dates for the search.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_flights(self) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    def _get_one_flight(self, departure_date, return_date) -> dict:
        raise NotImplementedError

    def _request_url(self, url) -> dict | None:
        """
        Requests url (json content) and returns the response in json format
        :return: Dict with json response or None
        """
        number_of_attemps = 4
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
            "Accept-Encoding": "application/json",
        }
        for attempts in range(number_of_attemps):
            try:
                LOGGER.debug(f"Requesting {url} for the {attempts} time.")
                response = requests.get(
                    url, headers=headers, timeout=15
                )
                response.raise_for_status()

                return self._convert_request_response_to_dict(response)

            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
            ) as error:
                code = None
                if error == requests.exceptions.HTTPError:
                    code = error.response.status_code
                    LOGGER.error(f"Http error code: {code}")

                LOGGER.warning(
                    f"Could not get the url. Trying it again in {str(attempts * 2)} "
                    f"seconds"
                )
                time.sleep(attempts * 2)
                continue

            except Exception as error:
                LOGGER.error(f"Error: {error}")
                LOGGER.error(f"Canceling requesting {url}")
                break

        return None

    @staticmethod
    def _convert_request_response_to_dict(response: requests.Response) -> dict | None:
        if "application/json" in response.headers["content-type"]:
            return json.loads(response.text)
        else:
            raise requests.exceptions.InvalidJSONError(
                "The url must return a json response."
            )


class LatamFinder(TicketFinder):
    def __init__(self, departure_date: str, origin: str, destination: str):
        super().__init__(departure_date, origin, destination)

    def _generate_travel_dates(self) -> None:
        """
            Generates all possible travel dates for the search.
            Latam: We search using multiple of 7 due to original response format
            total travel dates = 2 * number_of_total_searches
        """
        all_dates = [self.departure_date + timedelta(days = 7 * x) for x in range(0, self.number_of_total_searches)]
        trips_combinations = tuple(i for i in itertools.combinations_with_replacement(all_dates, 2))
        self.all_travel_dates = trips_combinations

    def get_all_flights(self):
        """
            Retrieves all possible flights and prices concurrently and saves to instance
            variable all_flights.
            Saves in the instance the all_flights and best_price

        """

        with Pool(processes = 16) as pool:
            list_of_responses = pool.starmap(self._get_one_flight, self.all_travel_dates)

        list_of_all_departure_dates = []
        for response in list_of_responses:
            if response.get('best_price') is not None:
                if response['best_price'] < self.best_price:
                    self.best_price = response['best_price']

                for departure_date in response['flights'].keys():
                    list_of_all_departure_dates.append(departure_date)
                    if self.all_flights.get(departure_date):
                        self.all_flights[departure_date].update(response['flights'][departure_date])
                    else:
                        self.all_flights[departure_date] = {arrival_date: 0 for arrival_date in list_of_all_departure_dates}
                        self.all_flights[departure_date].update(response['flights'][departure_date])

    def _get_one_flight(self, departure_date: datetime, return_date: datetime) -> dict | None:
        """
            Returns a formated response from a single latam request
            ** This request returns multiple dates due to the api in latam.

            :return: Dict: {best_price:float, flights: {departure_date: {arrival_date: price}}}
        """
        departure_date_str = departure_date.strftime("%Y-%m-%d")
        return_date_str = return_date.strftime("%Y-%m-%d")

        LOGGER.debug(f"{departure_date_str} -> {return_date_str}")
        url = self._generate_complete_url(departure_date_str, return_date_str)
        response = self._request_url(url)
        if response:
            flight = self._reformat_latam_response(response)
            return flight

    def _generate_complete_url(self, departure_date_str, return_date_str):
        return f"http://bff.latam.com/ws/proxy/booking-webapp-bff/v1/public/revenue" \
              f"/bestprices/roundtrip?departure={departure_date_str}&origin={self.origin}" \
              f"&destination={self.destination}&cabin=Y&country=BR&language=PT&home=pt_br" \
              f"&return={return_date_str}&adult=1&promoCode="

    @staticmethod
    def _reformat_latam_response(api_response: dict) -> dict:
        """
        Reformats latam response using departure date as key and a dict for return date with the
        date as key as well.

        :return: Dict: {best_price:float, flights: {departure_date: {arrival_date: price}}}
        """
        response = {"flights": {}}
        for dt_departure in api_response['bestPrices']:
            response['flights'][dt_departure["departureDate"]] = {}
            for dt_return in dt_departure["returnDates"]:
                if dt_return["available"]:
                    response['flights'][dt_departure["departureDate"]].update(
                        {dt_return["date"]: dt_return["price"]["amount"]}
                    )
                else:
                    response['flights'][dt_departure["departureDate"]].update({dt_return["date"]: 0})
        response['best_price'] = api_response.get('cheapestPrice')
        return response


if __name__ == "__main__":
    latam = LatamFinder("2022-12-01", "VIX", "CGH")
    latam.get_all_flights()
    print(latam.all_flights)
