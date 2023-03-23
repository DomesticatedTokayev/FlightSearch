#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import datetime

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

import datetime as dt

origin_iata_code = "LON"

today = dt.datetime.now()
today_date = today.strftime("%d/%m/%Y")
months_range = today + dt.timedelta(days=60)
months_range = months_range.strftime("%d/%m/%Y")


flight_search = FlightSearch()
destinations = DataManager()
notification_manager = NotificationManager()

destinations_data = destinations.get_destinations_from_sheet()

### Check if destinations have airport codes (Replace and update in google docs if not available)
for dst in destinations_data:
    if destinations.check_missing_city_codes(dst):
        temp_code = flight_search.get_code_by_city(dst["city"])
        destinations.update_city_code(dst, temp_code)


for dst in destinations_data:
    flight = flight_search.search_flights(origin_city_code=origin_iata_code,
                                          destination_city_code=dst["iataCode"],
                                          from_date=today_date,
                                          to_date=months_range)

    if flight is None:
        continue

    if flight.price < dst["lowestPrice"]:
        outbound = flight.out_date
        split_time = outbound.split("T")[0]
        split_time = split_time.split("-")
        outbound_day = datetime.date(int(split_time[0]), int(split_time[1]), int(split_time[2]))
        outbound_day = outbound_day.strftime("%d/%m/%Y")

        inbound = flight.return_date
        split_time = inbound.split("T")[0]
        split_time = split_time.split("-")
        inbound_day = datetime.date(int(split_time[0]), int(split_time[1]), int(split_time[2]))
        inbound_day = inbound_day.strftime("%d/%m/%Y")

        message = "Low price alert!\n"
        message += f"Only £{flight.price} to fly from" \
                   f" {flight.origin_city}-{flight.origin_airport} to " \
                   f"{flight.destination_city}-{flight.destination_airport}," \
                   f" from {outbound_day} to {inbound_day} \n"

        if flight.stop_overs > 0:
            message += f"Flight has {flight.stop_overs} stop over, via {flight.via_city}"

        notification_manager.send_message(message)
