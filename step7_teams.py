# ============================================================
# step7_teams.py
# WHAT  : Send a notification to Microsoft Teams via webhook
#
# SETUP (do this once — needs Teams access):
#   1. Open Microsoft Teams
#   2. Go to the channel you want notifications in
#   3. Click the 3-dot menu (...) next to the channel name
#   4. Click "Connectors" (or "Manage channel" → Connectors)
#   5. Find "Incoming Webhook" → click Configure
#   6. Give it a name (e.g. "Weather Bot") → click Create
#   7. Copy the Webhook URL → add to your .env file
# ============================================================

import os
import urllib.request
import urllib.error
import json
from dotenv import load_dotenv

load_dotenv()

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")


def send_teams_notification(record: dict) -> bool:
    """
    Send a Teams adaptive card notification with weather record details.

    Args:
        record: dict with keys { id, data, created_at }

    Returns:
        True if sent successfully, False otherwise
    """

    weather    = record["data"]
    record_id  = record["id"]
    created_at = record["created_at"]

    # Teams uses a simple JSON message card format
    payload = {
        "@type":      "MessageCard",
        "@context":   "https://schema.org/extensions",
        "summary":    f"Weather Report Saved | Record ID: {record_id}",
        "themeColor": "0A8EA0",
        "title":      f"Weather Report Saved — Record ID: {record_id}",
        "sections": [
            {
                "facts": [
                    {"name": "Saved At",     "value": str(created_at)},
                    {"name": "City",         "value": f"{weather['city']}, {weather['country']}"},
                    {"name": "Temperature",  "value": f"{weather['temperature_c']}C (Feels like {weather['feels_like_c']}C)"},
                    {"name": "Condition",    "value": weather["weather_desc"]},
                    {"name": "Humidity",     "value": f"{weather['humidity_percent']}%"},
                    {"name": "Wind Speed",   "value": f"{weather['wind_speed_kmph']} km/h"},
                ],
                "text": "A new weather record has been saved to the database and Excel report."
            }
        ]
    }

    try:
        print("[TEAMS] Sending notification...")
        data = json.dumps(payload).encode("utf-8")
        req  = urllib.request.Request(
            TEAMS_WEBHOOK_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            body   = response.read().decode("utf-8")
            status = response.status

        if status == 200 and body.strip() == "1":
            print("[TEAMS] Notification sent to Teams channel")
            return True
        else:
            print(f"[TEAMS] Unexpected response {status}: {body}")
            return False

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"[TEAMS] HTTP {e.code} error: {body}")
        return False
    except Exception as e:
        print(f"[TEAMS] Failed to send notification: {e}")
        return False


# ── Run this file directly to test ───────────────────────────
if __name__ == "__main__":
    test_record = {
        "id": 99,
        "created_at": "2025-01-15 10:30:00",
        "data": {
            "city": "KualaLumpur",
            "country": "Malaysia",
            "temperature_c": 32,
            "feels_like_c": 38,
            "humidity_percent": 80,
            "wind_speed_kmph": 15,
            "weather_desc": "Partly Cloudy",
            "visibility_km": 10,
            "scraped_at": "2025-01-15 10:30:00",
        }
    }
    send_teams_notification(test_record)
