import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv("./vars/.env")

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_AUTH")
        self._token = self._get_new_token()

    def _get_new_token(self):
        url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret,
        }
        response = requests.post(url, headers=headers, data=body)

        if response.status_code == 200:
            token_data = response.json()
            print(f"Your token is {token_data['access_token']}")
            print(f"Your token expires in {token_data['expires_in']} seconds")
            return token_data['access_token']
        else:
            print(f"Failed to get token: {response.status_code} {response.text}")
            return None

    def get_destination_code(self, city_name):
        if not self._token:
            print("No valid token available")
            return "No Token"

        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json"
        }
        query = {
            "keyword": city_name,
            "subType": "CITY,AIRPORT",
            "page[limit]": 1
        }
        response = requests.get(url="https://test.api.amadeus.com/v1/reference-data/locations", headers=headers,
                                params=query)

        if response.status_code == 200:
            try:
                code = response.json()["data"][0]['iataCode']
                return code
            except IndexError:
                print(f"IndexError: No airport code for {city_name}")
                return "N/A"
            except KeyError:
                print(f"KeyError: No airport code found for {city_name}")
                return "Not Found"
        else:
            print(f"Failed to get destination code: {response.status_code} {response.text}")
            return "Error"

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        """Searches for flight option between two cities on specified
        departure and return dates using the amadeus api"""

        # print(f"Using this token to check_flights() {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()

# # Create an instance of FlightSearch to test the API key and secret authentication
# flight_search = FlightSearch()
#
# # Test the get_destination_code method
# city_name = "New York"
# airport_code = flight_search.get_destination_code(city_name)
# print(f"The IATA code for {city_name} is {airport_code}")
