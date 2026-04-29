# ============================================================
# main.py
# WHAT  : Full automation pipeline — runs all 8 steps in order
#
# FLOW:
#   Step 1 → Scrape weather data from wttr.in
#   Step 2 → Save to Excel file
#   Step 3 → Store in SQLite database (as JSON)
#   Step 4 → Send email notification (Gmail SMTP)        [commented out — blocked]
#   Step 5 → Send Telegram bot notification
#   Step 6 → Send email notification via SendGrid
#   Step 7 → Send Microsoft Teams webhook notification
#   Step 8 → Send email notification via Outlook SMTP
#
# HOW TO RUN:
#   python main.py
#   python main.py --city "Penang"
# ============================================================

import sys
import argparse
from step1_scrape        import scrape_weather
from step2_excel         import save_to_excel
from step3_database      import init_db, save_to_db
# from step4_email       import send_notification          # Gmail — blocked by Dyson network
from step5_telegram      import send_telegram_notification
from step6_sendgrid      import send_sendgrid_notification
from step7_teams         import send_teams_notification
from step8_outlook       import send_outlook_notification


def run_pipeline(city: str = "KualaLumpur"):
    print("=" * 55)
    print("  Python Automation Pipeline")
    print("=" * 55)

    # ── STEP 1: Scrape ────────────────────────────────────────
    print("\n[STEP 1] Scraping weather data...")
    weather_data = scrape_weather(city)

    # ── STEP 2: Excel ─────────────────────────────────────────
    print("\n[STEP 2] Saving to Excel...")
    excel_path = save_to_excel(weather_data)

    # ── STEP 3: Database ──────────────────────────────────────
    print("\n[STEP 3] Storing in database...")
    init_db()
    record = save_to_db(weather_data)

    # ── STEP 4: Gmail (disabled — blocked by Dyson network) ───
    # print("\n[STEP 4] Sending Gmail notification...")
    # email_ok = send_notification(record)

    # ── STEP 5: Telegram ──────────────────────────────────────
    print("\n[STEP 5] Sending Telegram notification...")
    telegram_ok = send_telegram_notification(record)

    # ── STEP 6: SendGrid Email ────────────────────────────────
    # print("\n[STEP 6] Sending SendGrid email notification...")
    # sendgrid_ok = send_sendgrid_notification(record)

    # # ── STEP 7: Microsoft Teams ───────────────────────────────
    # print("\n[STEP 7] Sending Teams notification...")
    # teams_ok = send_teams_notification(record)

    # ── STEP 8: Outlook SMTP ──────────────────────────────────
    # print("\n[STEP 8] Sending Outlook email notification...")
    # outlook_ok = send_outlook_notification(record)

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  Pipeline Complete!")
    print("=" * 55)
    print(f"  City         : {weather_data['city']}, {weather_data['country']}")
    print(f"  Temperature  : {weather_data['temperature_c']}C | {weather_data['weather_desc']}")
    print(f"  Record ID    : {record['id']}")
    print(f"  Saved At     : {record['created_at']}")
    print(f"  Excel File   : {excel_path}")
    print(f"  Telegram     : {'Sent' if telegram_ok else 'Failed (check TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID)'}")
    # print(f"  SendGrid     : {'Sent' if sendgrid_ok else 'Failed (check SENDGRID_API_KEY)'}")
    # print(f"  Teams        : {'Sent' if teams_ok else 'Failed (check TEAMS_WEBHOOK_URL)'}")
    # print(f"  Outlook      : {'Sent' if outlook_ok else 'Failed (check OUTLOOK_SENDER_EMAIL / OUTLOOK_PASSWORD)'}")
    print("=" * 55)


# ── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather Automation Pipeline")
    parser.add_argument(
        "--city",
        type=str,
        default="KualaLumpur",
        help="City name to scrape weather for (default: KualaLumpur)"
    )
    args = parser.parse_args()
    run_pipeline(city=args.city)
