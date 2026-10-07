"""Download éCO2mix consumption data from the ODRÉ open data portal."""

import datetime as dt
from pathlib import Path

import requests

BASE_URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets"
HISTORY_DATASET = "eco2mix-national-cons-def"
COLUMNS = ("date_heure", "consommation", "prevision_j1", "nature")
TIMEOUT_SECONDS = 120
FIRST_YEAR = 2012
RAW_DIR = Path("data/raw/eco2mix")


def build_export_params(year: int) -> dict[str, str]:
    """Return the query parameters to export one calendar year (UTC)."""
    return {
        "select": ",".join(COLUMNS),
        "order_by": "date_heure",
        "timezone": "UTC",
        "where": f"date_heure >= date'{year}-01-01' and date_heure < date'{year + 1}-01-01'",
    }


def download_year(year: int, dest_dir: Path) -> Path:
    """Download one year of history as a CSV file and return its path."""
    url = f"{BASE_URL}/{HISTORY_DATASET}/exports/csv"
    params = build_export_params(year)
    response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"eco2mix_{year}.csv"
    dest.write_bytes(response.content)
    return dest


def download_history(dest_dir: Path = RAW_DIR) -> list[Path]:
    """Download every year from FIRST_YEAR to the current year.

    A year is skipped when its file already exists, except the current and
    the previous year, whose values can still be revised by RTE.
    """
    current_year = dt.datetime.now(dt.UTC).year
    paths = []
    for year in range(FIRST_YEAR, current_year + 1):
        dest = dest_dir / f"eco2mix_{year}.csv"
        if dest.exists() and year < current_year - 1:
            print(f"{year}: already downloaded, skipped")
            paths.append(dest)
            continue
        paths.append(download_year(year, dest_dir))
        print(f"{year}: downloaded")
    return paths


if __name__ == "__main__":
    download_history()
