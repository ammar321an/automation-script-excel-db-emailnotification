# ============================================================
# step4_email.py
# WHAT  : Send an email notification after data is saved
# HOW   : Use Python's built-in smtplib with Gmail SMTP
#
# IMPORTANT — Gmail App Password setup:
#   1. Turn on 2-Step Verification on your Google account
#   2. Go to: myaccount.google.com > Security > App Passwords
#   3. Select "Mail" and generate a password
#   4. Copy that 16-character password into your .env file
# ============================================================

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

SENDER_EMAIL    = os.getenv("SENDER_EMAIL")
APP_PASSWORD    = os.getenv("SENDER_APP_PASSWORD")
RECEIVER_EMAIL  = os.getenv("RECEIVER_EMAIL")


def send_notification(record: dict) -> bool:
    """
    Send an email notification with the record details.

    Args:
        record: dict with keys { id, data, created_at }

    Returns:
        True if sent successfully, False otherwise
    """

    weather = record["data"]
    record_id = record["id"]
    created_at = record["created_at"]

    # ── Build the email subject ───────────────────────────────
    subject = f"✅ Weather Report Saved | Record ID: {record_id}"

    # ── Build a clean HTML email body ────────────────────────
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #0A8EA0;">🌤️ Weather Report — Automation Script</h2>
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
                <td style="padding: 8px 12px;">{weather['temperature_c']}°C (Feels like {weather['feels_like_c']}°C)</td>
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
            This email was sent automatically by the Day 7 Python Automation Script.<br>
            📁 Excel report saved to: output/weather_report.xlsx
        </p>
    </body>
    </html>
    """

    # ── Compose the email ─────────────────────────────────────
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECEIVER_EMAIL
    msg.attach(MIMEText(body, "html"))

    # ── Connect to Gmail SMTP and send ────────────────────────
    try:
        print(f"[EMAIL] Connecting to Gmail SMTP...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Encrypt the connection
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"[EMAIL] ✅ Email sent to {RECEIVER_EMAIL}")
        return True

    except Exception as e:
        print(f"[EMAIL] ❌ Failed to send email: {e}")
        return False


# ── Run this file directly to test ───────────────────────────
if __name__ == "__main__":
    # Simulate a record for testing without running full pipeline
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
    send_notification(test_record)
