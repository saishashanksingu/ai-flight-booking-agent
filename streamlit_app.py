# streamlit_app.py
# ------------------------------------------------------------------
# Streamlit front-end for your AI Flight Booking Assistant
# ------------------------------------------------------------------

import streamlit as st
from flight_api import FlightAPI
from utils import (
    pick_cheapest,
    format_duration,
    
    build_booking_url,     # ← NEW helper (added to utils.py)
)
from ai_reasoning.decision_agent import should_book_now

st.set_page_config(page_title="AI Flight Booking Assistant", page_icon="✈️")
st.title("✈️ FareGenius.Ai - AI Flight Booking Assistant")

# ───────────────────────────────────────────────
# 1️⃣  INPUTS
# ───────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    origin = st.text_input("From (IATA)", placeholder="DEL").upper()
with col2:
    destination = st.text_input("To (IATA)", placeholder="BOM").upper()
with col3:
    date = st.date_input("Departure Date").strftime("%Y-%m-%d")

st.markdown("---")

# ───────────────────────────────────────────────
# 2️⃣  SEARCH BUTTON
# ───────────────────────────────────────────────
if st.button("🔍  Find Cheapest Flight"):

    # Validate inputs
    if not (origin and destination and date):
        st.error("Please fill in all fields.")
        st.stop()

    with st.spinner("Searching flights…"):
        flights = FlightAPI().search_flights(origin, destination, date)

    if not flights:
        st.warning("No flights found for the selected route/date.")
        st.stop()

    # ──────────────────────────────────────────
    # 3️⃣  PICK CHEAPEST OFFER
    # ──────────────────────────────────────────
    cheapest = pick_cheapest(flights)
    itin     = cheapest["itineraries"][0]
    seg0     = itin["segments"][0]
    seg_last = itin["segments"][-1]

    st.subheader("🛫 Cheapest Flight")
    colA, colB = st.columns(2)
    with colA:
        st.write(f"**Airline:** {seg0['carrierCode']}")
        st.write(f"**Price:** {cheapest['price']['total']} EUR")
        st.write(f"**Duration:** {format_duration(itin['duration'])}")
    with colB:
        st.write(f"**From:** {seg0['departure']['iataCode']}  \n"
                 f"{seg0['departure']['at']}")
        st.write(f"**To:** {seg_last['arrival']['iataCode']}  \n"
                 f"{seg_last['arrival']['at']}")

    # ──────────────────────────────────────────
    # 4️⃣  AI ADVICE
    # ──────────────────────────────────────────
    with st.spinner("Generating AI advice…"):
        advice = should_book_now(
            cheapest["price"]["total"],
            origin, destination, date,
            itin["duration"]
        )

    color = "green" if "book" in advice.lower() else "orange"
    st.markdown(
        f"<span style='color:{color};font-weight:bold'>🤖 {advice}</span>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ──────────────────────────────────────────
    # 5️⃣  BOOKING LINK (Kayak by default)
    # ──────────────────────────────────────────
    airline_code = seg0["carrierCode"]
    engine       = st.selectbox("Open on:", ["kayak", "skyscanner (support coming soon!!)"], index=0)

    booking_url = build_booking_url(
        origin, destination, date,
        airline=airline_code,
        engine=engine
    )

    # Streamlit ≥1.29 has link_button; fallback to markdown otherwise
    try:
        st.link_button("🛒  Book this flight", booking_url)
    except AttributeError:
        st.markdown(f"[🛒  Book this flight]({booking_url})")

    st.caption("Link opens in a new tab on the selected booking site.")
