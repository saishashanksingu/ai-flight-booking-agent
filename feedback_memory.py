import json
import os

FEEDBACK_FILE = "feedback.json"

def save_feedback(route, advice, user_response):
    feedback = {}
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            feedback = json.load(f)

    route_key = f"{route}"
    feedback_entry = {
        "advice": advice,
        "user_feedback": user_response
    }

    feedback.setdefault(route_key, []).append(feedback_entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback, f, indent=4)

def print_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        print("No feedback yet.")
        return

    with open(FEEDBACK_FILE, "r") as f:
        feedback = json.load(f)

    for route, entries in feedback.items():
        print(f"\n\U0001F6EB Route: {route}")
        for entry in entries:
            print(f"   → Advice: {entry['advice']}")
            print(f"   → User said: {entry['user_feedback']}")