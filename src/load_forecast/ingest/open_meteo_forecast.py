import datetime as dt
import json
import logging
import time
from pathlib import Path

import pandas as pd
import requests

from load_forecast.ingest.open_meteo import CITIES, PAUSE_SECONDS, TIMEOUT_SECONDS
from load_forecast.logging_setup import setup_logging

logger = logging.getLogger(__name__)
PREVIOUS_RUNS_URL = "https://previous-runs-api.open-meteo.com/v1/forecast"
RAW_DIR = Path("data/raw/open_meteo_forecast")
FIRST_YEAR = 2024


def download_city_year(city: str, year: int, dest_dir: Path = RAW_DIR) -> Path:
    """Download one year of hourly temperature for one city and return the file path."""
    latitude, longitude = CITIES[city]
    last_day = min(dt.date(year, 12, 31), dt.date.today() - dt.timedelta(days=1))
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": f"{year}-01-01",
        "end_date": last_day.isoformat(),
        "hourly": "temperature_2m_previous_day2",
        "timezone": "UTC",
    }
    response = requests.get(PREVIOUS_RUNS_URL, params=params, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{city}_{year}.json"
    dest.write_bytes(response.content)
    return dest


def read_raw_json(city: str, path: Path) -> pd.DataFrame:
    """Read one raw Open-Meteo file and return hourly rows shaped like the weather table."""
    data = json.loads(path.read_text())
    frame = pd.DataFrame(data["hourly"])
    frame["ts"] = pd.to_datetime(frame["time"], utc=True)
    frame["city"] = city
    frame = frame.rename(columns={"temperature_2m_previous_day2": "temperature_c"})
    return frame[["city", "ts", "temperature_c"]]


def download_all(dest_dir: Path = RAW_DIR) -> None:
    """Download every city and every year, skipping files that already exist.

    The current year is always downloaded again, because new days keep arriving.
    """
    current_year = dt.date.today().year
    for city in CITIES:
        for year in range(FIRST_YEAR, current_year + 1):
            dest = dest_dir / f"{city}_{year}.json"
            if dest.exists() and year < current_year:
                continue
            download_city_year(city, year, dest_dir)
            logger.info(f"{city} {year}: downloaded")
            time.sleep(PAUSE_SECONDS)


if __name__ == "__main__":
    setup_logging()
    download_all()
