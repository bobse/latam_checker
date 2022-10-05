import json
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import TestCase, mock
from unittest.mock import patch, Mock

import requests.exceptions
from requests import Timeout

from latam import LatamFinder

BASE_PATH = Path(__file__).resolve().parent


class TestAbsClass(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.departure_date = datetime.now().strftime("%Y-%m-%d")
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
            LatamFinder("2000-10-10", "CGH", "VIX")

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            LatamFinder("2022-35-10", "CGH", "VIX")

    def test_generate_travel_dates(self):
        test_latam = LatamFinder(self.departure_date, "CGH", "VIX")
        covered_days_in_search = (test_latam.number_of_total_searches - 1) * 7
        last_search_date = datetime.strptime(
            self.departure_date, "%Y-%m-%d"
        ) + timedelta(days=covered_days_in_search)
        self.assertEqual(last_search_date, test_latam.all_travel_dates[-1][-1])
        self.assertEqual(6, len(test_latam.all_travel_dates))

    @patch("latam.requests.get", side_effect=requests.exceptions.ConnectionError)
    def test_get_one_flight_connection_error(self, mock_requests):
        test_latam = LatamFinder(self.departure_date, "CGH", "VIX")
        test_url = test_latam._generate_complete_url("2022-10-10", "2022-11-11")
        self.assertEqual(None, test_latam._request_url(test_url))

    @patch("latam.requests.get", side_effect=requests.exceptions.RequestException)
    def test_get_one_flight_error_not_catch(self, mock_requests):
        test_latam = LatamFinder(self.departure_date, "CGH", "VIX")
        test_url = test_latam._generate_complete_url("2022-10-10", "2022-11-11")
        self.assertEqual(None, test_latam._request_url(test_url))

    @patch("latam.requests.get")
    def test_get_one_flight_ok(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.text = json.dumps(self.flights_response)
        mock_requests.return_value.headers = {"content-type": "application/json"}
        test_latam = LatamFinder(self.departure_date, "CGH", "VIX")
        response = test_latam._get_one_flight(
            datetime.strptime(self.departure_date, "%Y-%m-%d"),
            datetime.strptime(self.departure_date, "%Y-%m-%d"),
        )
        self.assertEqual(2701.84, response['flights']['2022-10-07']['2022-11-08'])
        self.assertEqual(1978.48, response['flights']['2022-10-13']['2022-11-14'])


if __name__ == "__main__":
    unittest.main()
