import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("PAYOUTS_TOKEN")

def get_average_price(origin, destination, period_month, currency="EUR"):
    url = "http://api.travelpayouts.com/v1/prices/calendar"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_date": period_month,
        "calendar_type": "departure_date",
        "currency": currency,
        "token": TOKEN
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    prices = [v["price"] for v in data.get("data", {}).values() if "price" in v]
    if not prices:
        return None, "No price data"
    return sum(prices) / len(prices), None
