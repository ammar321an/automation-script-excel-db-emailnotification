# ============================================================
# main.py
# WHAT  : Full automation pipeline — runs all 4 steps in order
#
# FLOW:
#   Step 1 → Scrape weather data from wttr.in
#   Step 2 → Save to Excel file
#   Step 3 → Store in SQLite database (as JSON)
#   Step 4 → Send email notification
#
# HOW TO RUN:
#   python main.py
#   python main.py --city "Penang"
# ============================================================

import sys
import argparse
from step1_scrape   import scrape_weather
from step2_excel    import save_to_excel
from step3_database import init_db, save_to_db
from step4_email    import send_notification


def run_pipeline(city: str = "KualaLumpur"):
    print("=" * 55)
    print("  🚀 Day 7 — Python Automation Pipeline")
    print("=" * 55)

    # ── STEP 1: Scrape ────────────────────────────────────────
    print("\n📡 STEP 1: Scraping weather data...")
    weather_data = scrape_weather(city)

    # ── STEP 2: Excel ─────────────────────────────────────────
    print("\n📊 STEP 2: Saving to Excel...")
    excel_path = save_to_excel(weather_data)

    # ── STEP 3: Database ──────────────────────────────────────
    print("\n🗄️  STEP 3: Storing in database...")
    init_db()
    record = save_to_db(weather_data)

    # ── STEP 4: Email ─────────────────────────────────────────
    print("\n📧 STEP 4: Sending email notification...")
    success = send_notification(record)

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  ✅ Pipeline Complete!")
    print("=" * 55)
    print(f"  City       : {weather_data['city']}, {weather_data['country']}")
    print(f"  Temperature: {weather_data['temperature_c']}°C | {weather_data['weather_desc']}")
    print(f"  Record ID  : {record['id']}")
    print(f"  Saved At   : {record['created_at']}")
    print(f"  Excel File : {excel_path}")
    print(f"  Email Sent : {'✅ Yes' if success else '❌ No (check .env credentials)'}")
    print("=" * 55)


# ── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Day 7 Weather Automation")
    parser.add_argument(
        "--city",
        type=str,
        default="KualaLumpur",
        help="City name to scrape weather for (default: KualaLumpur)"
    )
    args = parser.parse_args()
    run_pipeline(city=args.city)
