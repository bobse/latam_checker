import json
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import TestCase, mock
from unittest.mock import patch

import requests.exceptions
from validators import FlightData

from scrapers import LatamFinder

BASE_PATH = Path(__file__).resolve().parent


class TestAbsClass(TestCase):
    def _mock_response(
        self, status=200, content="CONTENT", json_data=None, raise_for_status=None
    ):
        """
        Mock response maker
        reference: https://gist.github.com/sahilsk/8ff32c378c13312e797ec2a7130767da
        """
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(return_value=json_data)
        return mock_resp

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.flight = FlightData(
            departure_date=datetime.now().strftime("%Y-%m-%d"),
            origin="CGH",
            destination="VIX",
        )
        cls.flights_response = {
            "bestPrices": [
                {
                    "departureDate": "2022-10-07",
                    "returnDates": [
                        {
                            "date": "2022-11-08",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-09",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-10",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-11",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-12",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-13",
                            "price": {"amount": 2677.2, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-14",
                            "price": {"amount": 2677.2, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                    ],
                },
                {
                    "departureDate": "2022-10-08",
                    "returnDates": [
                        {
                            "date": "2022-11-08",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-09",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-10",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-11",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-12",
                            "price": {"amount": 2701.84, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-13",
                            "price": {"amount": 2677.2, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-14",
                            "price": {"amount": 2677.2, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                    ],
                },
                {
                    "departureDate": "2022-10-09",
                    "returnDates": [
                        {
                            "date": "2022-11-08",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-09",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-10",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-11",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-12",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-13",
                            "price": {"amount": 2297.92, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-14",
                            "price": {"amount": 2297.92, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                    ],
                },
                {
                    "departureDate": "2022-10-10",
                    "returnDates": [
                        {
                            "date": "2022-11-08",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-09",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-10",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-11",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-12",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-13",
                            "price": {"amount": 2297.92, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-14",
                            "price": {"amount": 2297.92, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                    ],
                },
                {
                    "departureDate": "2022-10-11",
                    "returnDates": [
                        {
                            "date": "2022-11-08",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-09",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-10",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-11",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-12",
                            "price": {"amount": 2322.56, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-13",
                            "price": {"amount": 2297.92, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-14",
                            "price": {"amount": 2297.92, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                    ],
                },
                {
                    "departureDate": "2022-10-12",
                    "returnDates": [
                        {
                            "date": "2022-11-08",
                            "price": {"amount": 915.44, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-09",
                            "price": {"amount": 915.44, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-10",
                            "price": {"amount": 915.44, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-11",
                            "price": {"amount": 915.44, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-12",
                            "price": {"amount": 915.44, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-13",
                            "price": {"amount": 890.8, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-14",
                            "price": {"amount": 890.8, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                    ],
                },
                {
                    "departureDate": "2022-10-13",
                    "returnDates": [
                        {
                            "date": "2022-11-08",
                            "price": {"amount": 2003.12, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-09",
                            "price": {"amount": 2003.12, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-10",
                            "price": {"amount": 2003.12, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-11",
                            "price": {"amount": 2003.12, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-12",
                            "price": {"amount": 2003.12, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-13",
                            "price": {"amount": 1978.48, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                        {
                            "date": "2022-11-14",
                            "price": {"amount": 1978.48, "currency": "BRL"},
                            "availability": "AVAILABLE",
                            "available": True,
                            "notAvailable": False,
                        },
                    ],
                },
            ],
            "cheapestPrice": 890.8,
        }

    def test_older_date(self):
        with self.assertRaises(ValueError):
            test_flight = FlightData(
                departure_date="2000-10-10", origin="CGH", destination="VIX"
            )
            LatamFinder(test_flight)

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            test_flight = FlightData(
                departure_date="2000-35-10", origin="CGH", destination="VIX"
            )
            LatamFinder(test_flight)

    def test_generate_travel_dates(self):
        test_latam = LatamFinder(self.flight)
        covered_days_in_search = (test_latam._number_of_total_searches - 1) * 7
        last_search_date = self.flight.departure_date + timedelta(
            days=covered_days_in_search
        )
        self.assertEqual(last_search_date, test_latam._all_travel_dates[-1][-1])
        self.assertEqual(6, len(test_latam._all_travel_dates))

    @patch("scrapers.requests.get", side_effect=requests.exceptions.ConnectionError)
    def test_get_one_flight_connection_error(self, mock_requests):
        test_latam = LatamFinder(self.flight)
        test_url = test_latam._generate_complete_url("2022-10-10", "2022-11-11")
        self.assertEqual(None, test_latam._request_url(test_url))

    @patch("scrapers.requests.get", side_effect=requests.exceptions.RequestException)
    def test_get_one_flight_error_not_catch(self, mock_requests):
        test_latam = LatamFinder(self.flight)
        test_url = test_latam._generate_complete_url("2022-10-10", "2022-11-11")
        self.assertEqual(None, test_latam._request_url(test_url))

    @patch("scrapers.requests.get")
    def test_get_one_flight_ok(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.text = json.dumps(self.flights_response)
        mock_requests.return_value.headers = {"content-type": "application/json"}
        test_latam = LatamFinder(self.flight)
        response = test_latam._get_one_flight(
            self.flight.departure_date, self.flight.departure_date
        )
        self.assertEqual(2701.84, response["flights"]["2022-10-07"]["2022-11-08"])
        self.assertEqual(1978.48, response["flights"]["2022-10-13"]["2022-11-14"])

    @patch("scrapers.requests.get")
    def test_get_one_flight_404(self, mock_requests):
        mock_requests.return_value.status_code = 404
        mock_requests.return_value.raise_for_status = mock.Mock()
        mock_requests.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError()
        )
        mock_requests.return_value.text = json.dumps({"error": "some error"})
        mock_requests.return_value.headers = {"content-type": "application/json"}
        test_latam = LatamFinder(self.flight)
        response = test_latam._get_one_flight(
            self.flight.departure_date, self.flight.departure_date
        )
        self.assertEqual({}, response)

    @patch("scrapers.Pool")
    def test_get_all_flights_with_some_empty_responses(self, latam_mock):
        get_one_flight_response_test = {
            "flights": {"2022-04-22": {"2022-04-22": 258.0}},
            "best_price": 40,
        }
        mock_pool_instance = latam_mock.return_value.__enter__.return_value
        mock_pool_instance.starmap.return_value = [
            {},
            get_one_flight_response_test,
            {},
        ]
        test_latam = LatamFinder(self.flight)
        best_price, flights = test_latam.get_all_flights()
        mock_pool_instance.starmap.assert_called_once()
        self.assertEqual(get_one_flight_response_test["flights"], flights)
        self.assertEqual(get_one_flight_response_test["best_price"], best_price)

    @patch("scrapers.Pool")
    def test_get_all_flights_with_empty_responses(self, latam_mock):
        mock_pool_instance = latam_mock.return_value.__enter__.return_value
        mock_pool_instance.starmap.return_value = [
            {},
            {},
            {},
        ]
        test_latam = LatamFinder(self.flight)
        best_price, flights = test_latam.get_all_flights()
        mock_pool_instance.starmap.assert_called_once()
        self.assertEqual({}, flights)
        self.assertEqual(None, best_price)


if __name__ == "__main__":
    unittest.main()
