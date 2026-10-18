"""Load the actual consumption and the RTE forecast from the database."""

import pandas as pd

from load_forecast.db import read_sql


def load_actuals() -> pd.DataFrame:
    """Return consumption and RTE day-ahead forecast, indexed by UTC timestamp."""
    actuals = read_sql("SELECT ts, consumption_mw, forecast_d1_mw FROM consumption ORDER BY ts")
    actuals["ts"] = pd.to_datetime(actuals["ts"], utc=True)
    actuals = actuals.set_index("ts")
    return actuals.astype(float)
