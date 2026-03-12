# ============================================================
# step1_scrape.py
# WHAT  : Fetch weather data from wttr.in for Kuala Lumpur
# HOW   : Use requests to call the API, parse the JSON response
# ============================================================

import requests
import json
from datetime import datetime


def scrape_weather(city: str = "KualaLumpur") -> dict:
    """
    Scrape current weather for a given city from wttr.in.
    Returns a clean dictionary with the weather data.
    """

    # wttr.in supports JSON format via ?format=j1
    url = f"https://wttr.in/{city}?format=j1"

    print(f"[SCRAPE] Fetching weather for: {city}")
    print(f"[SCRAPE] URL: {url}")

    # Send GET request to the website
    response = requests.get(url, timeout=10)

    # Check if the request was successful (status code 200 = OK)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

    # Parse the JSON response
    raw = response.json()

    # Extract only the fields we need
    current = raw["current_condition"][0]
    nearest_area = raw["nearest_area"][0]

    weather_data = {
        "city": city,
        "country": nearest_area["country"][0]["value"],
        "temperature_c": int(current["temp_C"]),
        "feels_like_c": int(current["FeelsLikeC"]),
        "humidity_percent": int(current["humidity"]),
        "wind_speed_kmph": int(current["windspeedKmph"]),
        "weather_desc": current["weatherDesc"][0]["value"],
        "visibility_km": int(current["visibility"]),
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    print(f"[SCRAPE] Success! Temp: {weather_data['temperature_c']}°C | {weather_data['weather_desc']}")
    return weather_data


# ── Run this file directly to test ───────────────────────────
if __name__ == "__main__":
    data = scrape_weather("KualaLumpur")
    print("\n── Weather Data ──")
    print(json.dumps(data, indent=2))
