"""Connection to the PostgreSQL database."""

import os

import pandas as pd
import psycopg
from dotenv import load_dotenv


def connect() -> psycopg.Connection:
    """Open a connection using the variables defined in .env."""
    load_dotenv()
    return psycopg.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


def read_sql(query: str, params: tuple | None = None) -> pd.DataFrame:
    """Run a SQL query and return the result as a DataFrame."""
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = []
            for column in cursor.description:
                columns.append(column.name)
    return pd.DataFrame(rows, columns=columns)
