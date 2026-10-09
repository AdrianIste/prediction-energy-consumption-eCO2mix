"""Load raw éCO2mix files into the consumption table."""

from pathlib import Path

import pandas as pd
import psycopg

from load_forecast.db import connect
from load_forecast.ingest.eco2mix import RAW_DIR, read_raw_csv

UPSERT_SQL = """
    INSERT INTO consumption (ts, consumption_mw, forecast_d1_mw, nature)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (ts) DO UPDATE SET
        consumption_mw = EXCLUDED.consumption_mw,
        forecast_d1_mw = EXCLUDED.forecast_d1_mw,
        nature = EXCLUDED.nature,
        loaded_at = now()
"""


def to_rows(frame: pd.DataFrame) -> list[tuple]:
    """Turn a DataFrame into a list of tuples, with None for missing values."""
    return [
        tuple(None if pd.isna(value) else value for value in row)
        for row in frame.itertuples(index=False, name=None)
    ]


def load_file(conn: psycopg.Connection, path: Path) -> int:
    """Upsert one raw file into the consumption table and return the row count."""
    rows = to_rows(read_raw_csv(path))
    with conn.cursor() as cursor:
        cursor.executemany(UPSERT_SQL, rows)
    return len(rows)


def load_history(raw_dir: Path = RAW_DIR) -> int:
    """Upsert every raw file of the directory and return the total row count."""
    total = 0
    with connect() as conn:
        for path in sorted(raw_dir.glob("eco2mix_*.csv")):
            count = load_file(conn, path)
            print(f"{path.name}: {count} rows")
            total += count
    print(f"Total: {total} rows")
    return total


if __name__ == "__main__":
    load_history()
