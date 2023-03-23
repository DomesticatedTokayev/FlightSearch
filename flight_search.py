import requests
from flight_data import FlightData
import os

FLIGHT_SEARCH_ENDPOINT = os.environ.get("Flight_search_endpoint")
FLIGHT_LOCATE_ENDPOINT = os.environ.get("Flight_locate_endpoint") 

KIWI_API_KEY = "3T6eGI3mD8RdWEX_0-cmOWdyqldErA1l"
headers = {
    "apikey": KIWI_API_KEY
}

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.query = {}
        self.nights_in_dst_from = 7
        self.nights_in_dst_to = 28
        self.flight_type = "round"
        self.one_for_city = 1
        self.currency = "GBP"

    def search_flights(self, origin_city_code, destination_city_code, from_date, to_date):
        self.query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_date,
            "date_to": to_date,
            "nights_in_dst_from": self.nights_in_dst_from,
            "nights_in_dst_to": self.nights_in_dst_to,
            "flight_type": self.flight_type,
            "one_for_city": self.one_for_city,
            "curr": self.currency,
            "max_stopovers": 0
        }

        response = requests.get(url=FLIGHT_SEARCH_ENDPOINT, params=self.query, headers=headers)

        try:
            result = response.json()["data"][0]
        except IndexError:
            self.query["max_stopovers"] = 1
            response = requests.get(url=FLIGHT_SEARCH_ENDPOINT, params=self.query, headers=headers)

            try:
                data = response.json()["data"][0]
            except IndexError:
                # No flights found (Sometimes even if flights with step_overs exist. Tequilla's services limit this
                # to prevent webscraping)
                return
            else:
                flight_data = FlightData(price=data['price'],
                                         origin_city=data["route"][0]["cityFrom"],
                                         origin_airport=data["route"][0]['flyFrom'],
                                         destination_city=data["route"][1]['cityTo'],
                                         destination_airport=data["route"][1]["flyTo"],
                                         out_date=data["route"][0]['local_departure'],
                                         return_date=data["route"][2]['local_departure'],
                                         stop_overs=1,
                                         via_city=data["route"][0]["cityTo"]
                                         )
                return flight_data

        else:
            flight_data = FlightData(price=result['price'],
                                     origin_city=result['cityFrom'],
                                     origin_airport=result['flyFrom'],
                                     destination_city=result['cityTo'],
                                     destination_airport=result["flyTo"],
                                     out_date=result["route"][0]['local_departure'],
                                     return_date=result["route"][1]['local_departure']
                                     )
            return flight_data


    def check_prices(self, available_flights, destinations):
        cheap_flights = []

        for flight in available_flights:
            for dst in destinations:
                if dst["city"] == flight["Arrival City"]:
                    if flight["price"] <= dst["lowestPrice"]:
                        cheap_flights.append(flight)
        return cheap_flights

    def get_code_by_city(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city"
        }

        response = requests.get(url=FLIGHT_LOCATE_ENDPOINT, params=params,
                                headers=headers)
        # print(response.raise_for_status())
        result = response.json()["locations"]
        city_code = result[0]['code']
        return city_code

