# main.py – AI Smart Flight Finder with redirect-to-booking
from flight_api import FlightAPI
from utils import (
    pick_cheapest,
    print_flight,
    redirect_to_booking_site,
)
from ai_reasoning.decision_agent import should_book_now
from feedback_memory import save_feedback

from colorama import Fore, init
from dotenv import load_dotenv
from datetime import datetime
import os, cohere, sys

# ────────────────────────────────
load_dotenv()
init(autoreset=True)
# ────────────────────────────────


def get_detailed_advice(
    origin, destination, departure_date, duration, price, advice
):
    """Ask Cohere for a longer explanation."""
    try:
        days_until = (
            datetime.strptime(departure_date, "%Y-%m-%d").date()
            - datetime.today().date()
        ).days
    except Exception:
        days_until = "unknown"

    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    prompt = f"""
You are a smart travel assistant. The user is considering a flight:

• Route: {origin} → {destination}
• Departure: {departure_date}  (in {days_until} days)
• Duration: {duration}
• Price: {price} EUR

Earlier advice: “{advice}”

Give a more detailed explanation (2-4 sentences) on whether to
book or wait, referencing typical price trends and risk of delay.
"""
    resp = co.generate(model="command", prompt=prompt, max_tokens=200, temperature=0.7)
    print(f"\n📘 Detailed Advice:\n{resp.generations[0].text.strip()}")


def main():
    origin = input("Enter origin airport code: ").upper()
    destination = input("Enter destination airport code: ").upper()
    departure_date = input("Enter departure date (YYYY-MM-DD): ")

    # 1️⃣  Search via Amadeus
    flights = FlightAPI().search_flights(origin, destination, departure_date)
    if not flights:
        print("No flights found.")
        return

    # 2️⃣  Cheapest flight
    cheapest = pick_cheapest(flights)
    print_flight(cheapest)

    price = cheapest["price"]["total"]
    duration = cheapest["itineraries"][0]["duration"]

    # 3️⃣  AI recommendation
    try:
        advice = should_book_now(price, origin, destination, departure_date, duration)
    except Exception as e:
        print(f"AI error: {e}")
        advice = "No advice available"

    if "book" in advice.lower():
        print(f"\n\U0001F7E2 {Fore.GREEN}Advice from AI: {advice}")
    elif "wait" in advice.lower():
        print(f"\n\U0001F7E1 {Fore.YELLOW}Advice from AI: {advice}")
    else:
        print(f"\n\U0001F916 Advice from AI: {advice}")

    # 4️⃣  Feedback
    fb = input("\U0001F4AC Was this advice helpful? (yes/no/more detail): ").strip().lower()
    save_feedback(f"{origin}-{destination}", advice, fb)

    if fb == "more detail":
        get_detailed_advice(origin, destination, departure_date, duration, price, advice)

    # 5️⃣  Redirect to booking site (Kayak by default)
    if fb in {"yes", "more detail"}:
        airline = cheapest["itineraries"][0]["segments"][0]["carrierCode"]
        redirect_to_booking_site(
            origin, destination, departure_date, airline=airline, engine="kayak"  # or "skyscanner"
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)
