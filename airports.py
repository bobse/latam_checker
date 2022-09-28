import json
from pathlib import Path
from typing import Dict

BASE_PATH = Path(__file__).resolve().parent
AIRPORTS_FILE = f"{BASE_PATH}/airports.json"


def load_airports(filename: str = AIRPORTS_FILE) -> Dict:
	"""
	Loads iata airport codes for the flights
	:return: Dict -> {Iata Code:City Name | Airport Name}
	"""
	with open(filename, 'r') as file:
		cities = json.load(file)
	aiports = {city['iata']: f"{city['city']} | {city['name']}" for city in cities
	           if city['type'] == 'AIRPORT' and (city['countryAlpha2'] == 'BR' or city[
				'countryAlpha2'] == 'PT')}
	return aiports
