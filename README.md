# Day 7 — Python Automation Demo Project

## Project Structure

```
day7_demo/
├── main.py            ← Run this to execute the full pipeline
├── step1_scrape.py    ← Scrape weather data from wttr.in
├── step2_excel.py     ← Save data to Excel
├── step3_database.py  ← Store data in SQLite database
├── step4_email.py     ← Send email notification
├── requirements.txt   ← Python dependencies
├── .env               ← Your email credentials (DO NOT share this)
└── output/
    └── weather_report.xlsx  ← Generated Excel file
```

---

## Setup (Run Once)

**1. Create virtual environment**
```bash
python -m venv venv
```

**2. Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Setup your .env file**

Open `.env` and fill in:
```
SENDER_EMAIL=your_gmail@gmail.com
SENDER_APP_PASSWORD=xxxx xxxx xxxx xxxx
RECEIVER_EMAIL=your_gmail@gmail.com
```

> **How to get Gmail App Password:**
> 1. Enable 2FA at myaccount.google.com
> 2. Go to Security → App Passwords
> 3. Generate a password for "Mail"
> 4. Paste the 16-character password above

---

## How to Run

**Run full pipeline (default city: Kuala Lumpur)**
```bash
python main.py
```

**Run for a different city**
```bash
python main.py --city "Penang"
python main.py --city "London"
```

**Test each step individually**
```bash
python step1_scrape.py    # Test scraping only
python step2_excel.py     # Test Excel only
python step3_database.py  # Test database only
python step4_email.py     # Test email only (uses fake data)
```

---

## What the Script Does

```
wttr.in API
    ↓  (requests)
Weather Data Dict
    ↓  (openpyxl)
Excel File → output/weather_report.xlsx
    ↓  (sqlite3)
SQLite DB → weather.db  { id, data (JSON), created_at }
    ↓  (smtplib)
Email → "Record ID: 3 saved at 2025-01-15 10:30:00"
```

---

## Useful Commands

**View database contents (VS Code)**
- Install extension: SQLite Viewer
- Open `weather.db` file directly in VS Code

**View database (terminal)**
```bash
python -c "from step3_database import get_all_records; [print(dict(r)) for r in get_all_records()]"
```
