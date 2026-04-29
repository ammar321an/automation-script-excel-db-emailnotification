# ============================================================
# step6_sendgrid.py
# WHAT  : Send an email notification via SendGrid (not Gmail)
#
# SETUP (do this once):
#   1. Go to https://sendgrid.com → sign up for a free account
#   2. Free tier allows 100 emails/day — no credit card needed
#   3. Go to Settings → API Keys → Create API Key (Full Access)
#   4. Copy the key → add to your .env file
#   5. Verify a sender email:
#      Settings → Sender Authentication → Single Sender Verification
#      (use your own email as the sender)
#   6. Add the sender + receiver emails to your .env file
# ============================================================

import os
import urllib.request
import urllib.error
import json
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY      = os.getenv("SENDGRID_API_KEY")
SENDGRID_SENDER_EMAIL = os.getenv("SENDGRID_SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"


def send_sendgrid_notification(record: dict) -> bool:
    """
    Send an HTML email notification via SendGrid API.

    Args:
        record: dict with keys { id, data, created_at }

    Returns:
        True if sent successfully, False otherwise
    """

    weather    = record["data"]
    record_id  = record["id"]
    created_at = record["created_at"]

    subject = f"Weather Report Saved | Record ID: {record_id}"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #0A8EA0;">Weather Report — Automation Script</h2>
        <p>A new weather record has been successfully stored in the database.</p>

        <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
            <tr style="background-color: #0D1B2A; color: white;">
                <th style="padding: 8px 12px; text-align: left;">Field</th>
                <th style="padding: 8px 12px; text-align: left;">Value</th>
            </tr>
            <tr style="background-color: #f4f8f9;">
                <td style="padding: 8px 12px;"><b>Record ID</b></td>
                <td style="padding: 8px 12px;">{record_id}</td>
            </tr>
            <tr>
                <td style="padding: 8px 12px;"><b>Saved At</b></td>
                <td style="padding: 8px 12px;">{created_at}</td>
            </tr>
            <tr style="background-color: #f4f8f9;">
                <td style="padding: 8px 12px;"><b>City</b></td>
                <td style="padding: 8px 12px;">{weather['city']}, {weather['country']}</td>
            </tr>
            <tr>
                <td style="padding: 8px 12px;"><b>Temperature</b></td>
                <td style="padding: 8px 12px;">{weather['temperature_c']}C (Feels like {weather['feels_like_c']}C)</td>
            </tr>
            <tr style="background-color: #f4f8f9;">
                <td style="padding: 8px 12px;"><b>Condition</b></td>
                <td style="padding: 8px 12px;">{weather['weather_desc']}</td>
            </tr>
            <tr>
                <td style="padding: 8px 12px;"><b>Humidity</b></td>
                <td style="padding: 8px 12px;">{weather['humidity_percent']}%</td>
            </tr>
            <tr style="background-color: #f4f8f9;">
                <td style="padding: 8px 12px;"><b>Wind Speed</b></td>
                <td style="padding: 8px 12px;">{weather['wind_speed_kmph']} km/h</td>
            </tr>
        </table>

        <br>
        <p style="color: #888; font-size: 12px;">
            This email was sent automatically by the Python Automation Script.<br>
            Excel report saved to: output/weather_report.xlsx
        </p>
    </body>
    </html>
    """

    payload = {
        "personalizations": [
            {
                "to": [{"email": RECEIVER_EMAIL}],
                "subject": subject,
            }
        ],
        "from": {"email": SENDGRID_SENDER_EMAIL},
        "content": [{"type": "text/html", "value": html_body}],
    }

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type":  "application/json",
    }

    try:
        print("[SENDGRID] Sending email notification...")
        data = json.dumps(payload).encode("utf-8")
        req  = urllib.request.Request(SENDGRID_URL, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status

        if status == 202:
            print(f"[SENDGRID] Email sent to {RECEIVER_EMAIL}")
            return True
        else:
            print(f"[SENDGRID] Unexpected status code: {status}")
            return False

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"[SENDGRID] HTTP {e.code} error: {body}")
        return False
    except Exception as e:
        print(f"[SENDGRID] Failed to send email: {e}")
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
    send_sendgrid_notification(test_record)
