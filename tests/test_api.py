import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import TestCase, mock

from fastapi import status
from fastapi.testclient import TestClient

from airports import load_airports
from main import app

BASE_PATH = Path(__file__).resolve().parent


class TestAirports(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.client = TestClient(app)

    def test_get_aiport_list(self):
        loaded_airports = load_airports()
        response = self.client.get("/airports")
        self.assertEqual(loaded_airports, response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_file(self):
        self.assertEqual(load_airports("nofile.json"), [])

    def test_404_airport_list_empty(self):
        with mock.patch("main.load_airports") as mock_load_airports:
            mock_load_airports.return_value = []
            response = self.client.get("/airports")
            self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestFlights(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.departure_date = (timedelta(days=3) + datetime.now()).strftime("%Y-%m-%d")
        cls.origin = "CGH"
        cls.destination = "VIX"
        cls.client = TestClient(app)
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

    def test_get_flights_200(self):
        with mock.patch("main.LatamFinder.get_all_flights") as mock_latam:
            mock_best_price = 0
            mock_latam.return_value = mock_best_price, self.flights_response
            response = self.client.get(
                f"/{self.departure_date}/{self.origin}/{self.destination}"
            )
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertEqual(
                mock_best_price, response.json()["best_price"]
            )
            self.assertEqual(
                self.flights_response, response.json()["flights"]
            )

    def test_no_best_price_404(self):
        with mock.patch("main.LatamFinder.get_all_flights") as mock_latam:
            mock_best_price = None
            mock_latam.return_value = mock_best_price, {}
            response = self.client.get(
                f"/{self.departure_date}/{self.origin}/{self.destination}"
            )
            self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_invalid_date_400(self):
        with mock.patch("main.LatamFinder") as mock_latam:
            response = self.client.get(f"/2000-01-01/{self.origin}/{self.destination}")
            self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
            self.assertIn('departure_date', response.json()['detail'][0]['loc'])

    def test_same_airport_400(self):
        with mock.patch("main.LatamFinder") as mock_latam:
            response = self.client.get(
                f"/{self.departure_date}/{self.origin}/{self.origin}"
            )
            self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
            self.assertIn('destination', response.json()['detail'][0]['loc'])

    def test_airport_not_in_database_400(self):
        with mock.patch("main.LatamFinder") as mock_latam:
            response = self.client.get(f"/{self.departure_date}/XYZ/ZYX")
            self.assertIn("not found", response.text)
            self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


if __name__ == "__main__":
    unittest.main()
