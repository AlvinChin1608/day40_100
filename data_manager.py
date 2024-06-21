import requests
import os
from dotenv import load_dotenv

# Load environment variable from the .env file
load_dotenv("./vars/.env")

SHEETY_PRICES_ENDPOINT = os.getenv("S_ENDPOINT")
SHEETY_BASIC_TOKEN = os.getenv("S_TOKEN")
SHEETY_USERS_ENDPOINT = os.getenv("SHEETY_USERS_ENDPOINT")

class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.basic_auth_headers = {
            "Authorization": f"Basic {SHEETY_BASIC_TOKEN}"
        }
        self.destination_data = {}
        self.customer_data = {}
        self.users_endpoint = SHEETY_USERS_ENDPOINT

    def get_destination_data(self):
        # 2. Use the sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=self.basic_auth_headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}", json=new_data,
                                    headers=self.basic_auth_headers)
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, headers=self.basic_auth_headers)
        response.raise_for_status()
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data

