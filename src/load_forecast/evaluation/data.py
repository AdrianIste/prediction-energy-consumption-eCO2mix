"""Load the actual consumption and the RTE forecast from the database."""

import datetime as dt

import pandas as pd

from load_forecast.db import read_sql


def load_actuals() -> pd.DataFrame:
    """Return consumption and RTE day-ahead forecast, indexed by UTC timestamp."""
    actuals = read_sql("SELECT ts, consumption_mw, forecast_d1_mw FROM consumption ORDER BY ts")
    actuals["ts"] = pd.to_datetime(actuals["ts"], utc=True)
    actuals = actuals.set_index("ts")
    return actuals.astype(float)


def load_temperature() -> pd.Series:
    """Return the hourly national temperature: the mean of the ten cities."""
    temperature = read_sql(
        """
        SELECT ts, avg(temperature_c) AS temperature_c
        FROM weather
        GROUP BY ts
        ORDER BY ts
        """
    )
    temperature["ts"] = pd.to_datetime(temperature["ts"], utc=True)
    return temperature.set_index("ts")["temperature_c"].astype(float)


def load_temperature_forecast() -> pd.Series:
    """Return the hourly national temperature forecast made 48 hours ahead: the mean of the ten
    cities."""
    temperature = read_sql(
        """
        SELECT ts, avg(temperature_c) AS temperature_c
        FROM weather_forecast
        GROUP BY ts
        ORDER BY ts
        """
    )
    temperature["ts"] = pd.to_datetime(temperature["ts"], utc=True)
    return temperature.set_index("ts")["temperature_c"].astype(float)


def load_temperature_daily(issued_on: dt.date) -> pd.Series:
    """Return the hourly national temperature forecast fetched on a given day."""
    temperature = read_sql(
        """
        SELECT ts, avg(temperature_c) AS temperature_c
        FROM weather_forecast_daily
        WHERE issued_on = %s
        GROUP BY ts
        ORDER BY ts
        """,
        (issued_on,),
    )
    temperature["ts"] = pd.to_datetime(temperature["ts"], utc=True)
    return temperature.set_index("ts")["temperature_c"].astype(float)
