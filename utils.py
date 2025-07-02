# utils.py
import webbrowser
from datetime import datetime

# ─────────────────────────────────────────────
# 1) FLIGHT-PICKING HELPERS
# ─────────────────────────────────────────────
def pick_cheapest(flights):
    """Return the offer object with the lowest total price."""
    return min(flights, key=lambda f: float(f["price"]["total"]))


def print_flight(flight: dict):
    """Pretty-print key details of a flight offer."""
    itin = flight["itineraries"][0]
    seg0 = itin["segments"][0]
    seg_last = itin["segments"][-1]

    print("\n Cheapest Flight Found:")
    print(f"Airline: {seg0['carrierCode']}")
    print(f"Price: {flight['price']['total']} EUR")
    print(f"Duration: {itin['duration']}")
    print(
        f"From: {seg0['departure']['iataCode']} at {seg0['departure']['at']}\n"
        f"To:   {seg_last['arrival']['iataCode']} at {seg_last['arrival']['at']}"
    )

# ─────────────────────────────────────────────
# 2) BOOKING-SITE REDIRECT
# ─────────────────────────────────────────────
def redirect_to_booking_site(
    origin: str,
    destination: str,
    date: str,
    airline: str | None = None,
    engine: str = "kayak",
):
    """
    Open a browser tab pre-filled with the user’s flight search.

    engine = "kayak" (default) | "skyscanner" | fallback → Google search
    """

    engine = engine.lower()

    if engine == "kayak":
        # Kayak deep-link:  /flights/ORIG-DST/YYY-MM-DD
        url = f"https://www.kayak.com/flights/{origin}-{destination}/{date}?sort=price_a"
        if airline:
            url += f"&fs=airlines={airline}"

    elif engine == "skyscanner":
        # Skyscanner format uses YYMMDD with no dashes.
        compact_date = datetime.strptime(date, "%Y-%m-%d").strftime("%y%m%d")
        url = (
            f"https://www.skyscanner.co.in/transport/flights/"
            f"{origin}/{destination}/{compact_date}/"
        )
        if airline:
            url += f"?adults=1&airlinecode={airline}"

    else:  # fallback Google search
        url = (
            "https://www.google.com/search?q="
            f"{origin}+to+{destination}+flights+{date}+{airline or ''}"
        )

    print(f"\n🔗  Opening booking site in your browser…\n{url}\n")
    webbrowser.open_new_tab(url)

# utils.py

def format_duration(duration):
    """
    Converts ISO 8601 duration format (e.g., PT3H45M) to '3h 45m'.
    """
    duration = duration.replace("PT", "")
    hours = minutes = ""

    if "H" in duration:
        parts = duration.split("H")
        hours = parts[0]
        duration = parts[1] if len(parts) > 1 else ""
    if "M" in duration:
        minutes = duration.replace("M", "")

    formatted = ""
    if hours:
        formatted += f"{hours}h "
    if minutes:
        formatted += f"{minutes}m"

    return formatted.strip()

# utils.py  (add at end)

def build_booking_url(origin, destination, date, airline=None, engine="kayak"):
    """
    Return a deep-link URL (without opening a browser).
    """
    engine = engine.lower()

    if engine == "kayak":
        url = f"https://www.kayak.com/flights/{origin}-{destination}/{date}?sort=price_a"
        if airline:
            url += f"&fs=airlines={airline}"
    elif engine == "skyscanner":
        from datetime import datetime
        compact = datetime.strptime(date, "%Y-%m-%d").strftime("%y%m%d")
        url = (
            f"https://www.skyscanner.co.in/transport/flights/"
            f"{origin}/{destination}/{compact}/"
        )
        if airline:
            url += f"?adults=1&airlinecode={airline}"
    else:
        url = (
            "https://www.google.com/search?q="
            f"{origin}+to+{destination}+flights+{date}+{airline or ''}"
        )
    return url
