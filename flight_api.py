import os
import requests
from dotenv import load_dotenv

load_dotenv()

class FlightAPI:
    def __init__(self):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.flight_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        self.access_token = self.get_access_token()

    def get_access_token(self):
        response = requests.post(self.token_url, data={
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        })
        return response.json()["access_token"]

    def search_flights(self, origin, destination, date):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": date,
            "adults": 1,
            "max": 10
        }
        response = requests.get(self.flight_url, headers=headers, params=params)
        return response.json().get("data", [])