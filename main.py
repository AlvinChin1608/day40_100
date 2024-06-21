# 4. pass the data back to main, so you can print data in main
from data_manager import DataManager
import time
from flight_search import FlightSearch
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# Create an instance of NotificationManager
notification_manager = NotificationManager()

# Create a DataManager instance to interact with the Google Sheet
data_manager = DataManager()
flight_search = FlightSearch()

# Set your origin airport
ORIGIN_CITY_IATA = "LON"

# Retrieve destination data from the Google Sheet
sheet_data = data_manager.get_destination_data()
print(sheet_data)

# 5. In main.py check if sheet_data contains any values for the "iataCode" key.
# Check if the IATA Codes column is empty in the Google Sheet
if sheet_data[0]["iataCode"] == "":
    flight_search = FlightSearch()

    # Iterate through each city in the destination data
    # and fetch the corresponding IATA code using the FlightSearch class
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row['city'])
        # slowing down requests to avoid rate limit
        time.sleep(2)
    print(f"sheet_data:\n {sheet_data}")

    # Update the Google Sheet with the new IATA codes
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

# ==================== Retrieve your customer emails ====================

customer_data = data_manager.get_customer_emails()
# Verify the name of your email column in your sheet. Yours may be different from mine
customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]
# print(f"Your email list includes {customer_email_list}")

# ==================== Search for Flights ====================

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today,
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)

    # Check for direct flights
    if cheapest_flight.price == "N/A":
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        stopover_flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: £{cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")
        message = (
            f"Low price alert! Only £{cheapest_flight.price} to fly "
            f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
            f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )
        notification_manager.send_whatsapp(message_body=message)

        # Send emails to everyone on the list
        notification_manager.send_emails(email_list=customer_email_list, email_body=message)

# https://docs.google.com/spreadsheets/d/1nPTyNo2Nb9c9J-BQWFlBvtxhH-N2-r_51QJbuvpxCcQ/edit?usp=sharing
