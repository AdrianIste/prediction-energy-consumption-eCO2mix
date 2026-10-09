"""Connection to the PostgreSQL database."""

import os

import psycopg
from dotenv import load_dotenv


def connect() -> psycopg.Connection:
    """Open a connection using the variables defined in .env."""
    load_dotenv()
    return psycopg.connect(
        host="localhost",
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
