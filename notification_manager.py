import smtplib
from email.message import EmailMessage
import datetime
from flight_data import FlightData
import os

GMAIL_CODE = "smtp.gmail.com"
SENDER_EMAIL = os.environ.get("Sender_email")
EMAIL_KEY = os.environ.get("Email_key")
RECEIVER_EMAIL = os.environ.get("Receiver_email")

class NotificationManager:
    def send_message(self, flight_message):

        message = flight_message

        msg = EmailMessage()
        msg.set_content(message)

        msg['Subject'] = "Cheap Flights Alert"
        msg["from"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        # with smtplib.SMTP(GMAIL_CODE) as connection:
        #     connection.starttls()
        #     connection.login(SENDER_EMAIL, EMAIL_KEY)
        #     connection.send_message(msg)

        print(f"Message Sent: {message}")


    def get_emails(self):
        pass

    def format_flight(self, flight):

        outbound = flight['return_date']
        split_time = outbound.split("T")[0]
        split_time = split_time.split("-")
        outbound_day = datetime.date(int(split_time[0]), int(split_time[1]), int(split_time[2]))
        outbound_day = outbound_day.strftime("%d/%m/%Y")

        inbound = flight['return_date']
        split_time = inbound.split("T")[0]
        split_time = split_time.split("-")
        inbound_day = datetime.date(int(split_time[0]), int(split_time[1]), int(split_time[2]))
        inbound_day = inbound_day.strftime("%d/%m/%Y")

        message = "Low price alert!\n"
        message += f"Only £{flight['price']} to fly from" \
               f" {flight['Departure City']}-{flight['Departure Airport IATA Code']} to " \
               f"{flight['Arrival City']}-{flight['Arrival Airport IATA Code']}," \
               f" from {outbound_day} to {inbound_day} \n\n"

        return message
