"""Fetch each morning the temperature forecast of the ten cities and store it."""

import datetime as dt
import logging
import time

import pandas as pd
import requests

from load_forecast.db import connect
from load_forecast.ingest.load_consumption import to_rows
from load_forecast.ingest.open_meteo import CITIES, PAUSE_SECONDS, TIMEOUT_SECONDS
from load_forecast.logging_setup import setup_logging

logger = logging.getLogger(__name__)

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
FORECAST_DAYS = 3

UPSERT_SQL = """
    INSERT INTO weather_forecast_daily (city, ts, issued_on, temperature_c)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (city, ts, issued_on) DO UPDATE SET
        temperature_c = EXCLUDED.temperature_c,
        loaded_at = now()
"""


def fetch_city_forecast(city: str) -> pd.DataFrame:
    """Return the hourly temperature forecast of one city for the next days."""
    latitude, longitude = CITIES[city]
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": FORECAST_DAYS,
        "timezone": "UTC",
    }
    response = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    frame = pd.DataFrame(response.json()["hourly"])
    frame["ts"] = pd.to_datetime(frame["time"], utc=True)
    frame["city"] = city
    frame = frame.rename(columns={"temperature_2m": "temperature_c"})
    return frame[["city", "ts", "temperature_c"]]


def load_daily_forecast(issued_on: dt.date | None = None) -> int:
    """Fetch the forecast of every city and upsert it, tagged with the issue day."""
    issued_on = issued_on or dt.date.today()
    total = 0
    with connect() as conn:
        for city in CITIES:
            frame = fetch_city_forecast(city)
            frame.insert(2, "issued_on", issued_on)
            rows = to_rows(frame)
            with conn.cursor() as cursor:
                cursor.executemany(UPSERT_SQL, rows)
            total += len(rows)
            logger.info(f"{city}: {len(rows)} hours")
            time.sleep(PAUSE_SECONDS)
    logger.info(f"Total: {total} rows issued on {issued_on}")
    return total


if __name__ == "__main__":
    setup_logging()
    load_daily_forecast()
