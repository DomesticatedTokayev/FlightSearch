import requests
import pandas as pd
from flight_search import FlightSearch
import os

SHEETY_ENDPOINT = os.environ.get("Sheety_endpoint")
SHEETY_USERS_ENDPOINT = os.environ.get("Sheety_users_endpoint")

headers = {
    "Authorization": SHEETY_BEARER_TOKEN,
    "Content-Type": "application/json"
}

class DataManager:
    def __init__(self):
        self.destinations = {}

    def get_destinations_from_sheet(self):
        # ## Use local data (Sheety has request limit for free plan)
        # response = requests.get(url=SHEETY_ENDPOINT, headers=headers)
        # print(response.raise_for_status())
        # self.destinations = response.json()["prices"]

        ##Add iata codes (and use this dict instead of sheety site (request limit reached)
        result = {'prices': [{'city': 'Paris', 'iataCode': 'PAR', 'id': 2, 'lowestPrice': 54},
                             {'city': 'Berlin', 'iataCode': 'BER', 'id': 3, 'lowestPrice': 42},
                             {'city': 'Sydney', 'iataCode': 'SYD', 'id': 5, 'lowestPrice': 551},
                             {'city': 'Istanbul', 'iataCode': 'IST', 'id': 6, 'lowestPrice': 95},
                             {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'id': 7, 'lowestPrice': 414},
                             {'city': 'New York', 'iataCode': 'NYC', 'id': 8, 'lowestPrice': 240},
                             {'city': 'San Francisco', 'iataCode': 'SFO', 'id': 9, 'lowestPrice': 260},
                             {'city': 'Cape Town', 'iataCode': 'CPT', 'id': 10, 'lowestPrice': 378},
                             {'city': 'Bali', 'iataCode': 'DPS', 'id': 501, 'lowestPrice': 378},
                             {'city': 'Tokyo', 'iataCode': 'TYO', 'id': 4, 'lowestPrice': 500},
                             {'city': 'South Korea', 'iataCode': 'ICN', 'id': 4, 'lowestPrice': 500}
                            ]
                  }
        self.destinations = result["prices"]
        return self.destinations

    def update_city_code(self, flight, code):
        param = {
            "price": {
                "iataCode": code
            }
        }
        print(f"{flight}, {code}")

        ## Disabled, due to max request reach
        response = requests.put(url=f"{SHEETY_ENDPOINT}/{flight['id']}", json=param, headers=headers)
        print(response.raise_for_status())
        result = response.json()
        print(response.text)

    def check_missing_city_codes(self, destination) -> bool:
        if destination["iataCode"] == "":
            return True
        return False
