# ============================================================
# step8_outlook.py
# WHAT  : Send an email notification via Outlook SMTP
#
# SETUP (do this once):
#   1. Make sure you have an Outlook / Hotmail account
#      (create free at outlook.com if you don't have one)
#   2. Add your Outlook email + password to your .env file
#   3. If login fails, check that your account allows SMTP:
#      outlook.com → Settings → Mail → Sync email → POP and IMAP
#      Make sure SMTP AUTH is not disabled
# ============================================================

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

OUTLOOK_SENDER_EMAIL   = os.getenv("OUTLOOK_SENDER_EMAIL")
OUTLOOK_PASSWORD       = os.getenv("OUTLOOK_PASSWORD")
OUTLOOK_RECEIVER_EMAIL = os.getenv("OUTLOOK_RECEIVER_EMAIL")

OUTLOOK_SMTP_HOST = "smtp-mail.outlook.com"
OUTLOOK_SMTP_PORT = 587


def send_outlook_notification(record: dict) -> bool:
    """
    Send an HTML email notification via Outlook SMTP.

    Args:
        record: dict with keys { id, data, created_at }

    Returns:
        True if sent successfully, False otherwise
    """

    weather    = record["data"]
    record_id  = record["id"]
    created_at = record["created_at"]

    subject = f"Weather Report Saved | Record ID: {record_id}"

    body = f"""
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

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = OUTLOOK_SENDER_EMAIL
    msg["To"]      = OUTLOOK_RECEIVER_EMAIL
    msg.attach(MIMEText(body, "html"))

    try:
        print(f"[OUTLOOK] Connecting to {OUTLOOK_SMTP_HOST}:{OUTLOOK_SMTP_PORT}...")
        with smtplib.SMTP(OUTLOOK_SMTP_HOST, OUTLOOK_SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(OUTLOOK_SENDER_EMAIL, OUTLOOK_PASSWORD)
            server.sendmail(OUTLOOK_SENDER_EMAIL, OUTLOOK_RECEIVER_EMAIL, msg.as_string())
        print(f"[OUTLOOK] Email sent to {OUTLOOK_RECEIVER_EMAIL}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[OUTLOOK] Authentication failed — check OUTLOOK_SENDER_EMAIL and OUTLOOK_PASSWORD in .env")
        return False
    except Exception as e:
        print(f"[OUTLOOK] Failed to send email: {e}")
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
    send_outlook_notification(test_record)
