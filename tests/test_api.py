import itertools
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

    def test_get_flights_200(self):
        with mock.patch("main.get_all_dates") as mock_latam_get_all_dates:
            mock_latam_get_all_dates.return_value = (
                {
                    "2022-10-12": {"2022-10-12": 1530.68, "2022-10-13": 2061.2},
                    "2022-10-13": {"2022-10-12": 0, "2022-10-13": 2061.2},
                },
                1530.68,
            )
            response = self.client.get(
                f"/{self.departure_date}/{self.origin}/{self.destination}"
            )
            self.assertEqual(
                status.HTTP_200_OK,
                response.status_code,
            )
            self.assertEqual(
                4,
                len(
                    list(
                        itertools.chain.from_iterable(response.json()["flights_matrix"])
                    )
                ),
            )
            self.assertEqual(1530.68, response.json()["best_price"])
            self.assertEqual({'0': '2022-10-12', '1': "2022-10-13"}, response.json()["key_map"])


if __name__ == "__main__":
    unittest.main()
