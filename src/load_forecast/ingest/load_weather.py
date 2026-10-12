"""Load raw Open-Meteo files into the weather table."""

import logging
from pathlib import Path

import psycopg

from load_forecast.db import connect
from load_forecast.ingest.load_consumption import to_rows
from load_forecast.ingest.open_meteo import CITIES, RAW_DIR, read_raw_json
from load_forecast.logging_setup import setup_logging

logger = logging.getLogger(__name__)
UPSERT_SQL = """
    INSERT INTO weather (city, ts, temperature_c)
    VALUES (%s, %s, %s)
    ON CONFLICT (city, ts) DO UPDATE SET
        temperature_c = EXCLUDED.temperature_c,
        loaded_at = now()
"""


def load_file(conn: psycopg.Connection, city: str, path: Path) -> int:
    """Upsert one raw file into the weather table and return the row count."""
    rows = to_rows(read_raw_json(city, path))
    with conn.cursor() as cursor:
        cursor.executemany(UPSERT_SQL, rows)
    return len(rows)


def load_all(raw_dir: Path = RAW_DIR) -> int:
    """Upsert every raw file of every city and return the total row count."""
    total = 0
    with connect() as conn:
        for city in CITIES:
            for path in sorted(raw_dir.glob(f"{city}_*.json")):
                total += load_file(conn, city, path)
            logger.info(f"{city}: loaded")
    logger.info(f"Total: {total} rows")
    return total


if __name__ == "__main__":
    setup_logging()
    load_all()
