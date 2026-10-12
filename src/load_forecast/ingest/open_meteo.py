"""Download hourly weather data from the Open-Meteo archive API."""

import datetime as dt
import json
import time
from pathlib import Path

import pandas as pd
import requests

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
RAW_DIR = Path("data/raw/open_meteo")
TIMEOUT_SECONDS = 120
FIRST_YEAR = 2012
PAUSE_SECONDS = 3

CITIES = {
    "paris": (48.86, 2.35),
    "lyon": (45.76, 4.84),
    "marseille": (43.30, 5.37),
    "toulouse": (43.60, 1.44),
    "bordeaux": (44.84, -0.58),
    "nantes": (47.22, -1.55),
    "lille": (50.63, 3.06),
    "strasbourg": (48.57, 7.75),
    "rennes": (48.12, -1.68),
    "nice": (43.71, 7.26),
}


def download_city_year(city: str, year: int, dest_dir: Path = RAW_DIR) -> Path:
    """Download one year of hourly temperature for one city and return the file path."""
    latitude, longitude = CITIES[city]
    last_day = min(dt.date(year, 12, 31), dt.date.today() - dt.timedelta(days=1))
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": f"{year}-01-01",
        "end_date": last_day.isoformat(),
        "hourly": "temperature_2m",
        "timezone": "UTC",
    }
    response = requests.get(ARCHIVE_URL, params=params, timeout=TIMEOUT_SECONDS)
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
    frame = frame.rename(columns={"temperature_2m": "temperature_c"})
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
            print(f"{city} {year}: downloaded")
            time.sleep(PAUSE_SECONDS)


if __name__ == "__main__":
    download_all()
