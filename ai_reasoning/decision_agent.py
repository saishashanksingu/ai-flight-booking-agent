import os
import cohere
from dotenv import load_dotenv
from datetime import datetime
from price_compare import get_average_price

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def should_book_now(price, origin, destination, departure_date, duration):
    try:
        today = datetime.today().date()
        dep_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
        days_until_departure = (dep_date - today).days
    except Exception:
        days_until_departure = "unknown"

    try:
        price_float = float(price)
        avg_price, error = get_average_price(origin, destination, departure_date[:7])

        if error:
            price_hint = "Real-time price comparison unavailable."
        else:
            if price_float < 0.85 * avg_price:
                price_hint = f"This is cheaper than the average ({avg_price:.2f} EUR)."
            elif price_float > 1.15 * avg_price:
                price_hint = f"This is more expensive than the average ({avg_price:.2f} EUR)."
            else:
                price_hint = f"This is close to the average price ({avg_price:.2f} EUR)."
    except:
        price_hint = ""

    prompt = f"""
    The user is considering a flight from {origin} to {destination}.
    The flight costs {price} EUR, has a duration of {duration}, and departs in {days_until_departure} days.
    {price_hint}
    Based on this, should the user book now or wait?
    Respond with one confident sentence.
    """

    try:
        response = co.generate(
            model='command',
            prompt=prompt,
            max_tokens=50,
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error getting AI advice from Cohere: {str(e)}"