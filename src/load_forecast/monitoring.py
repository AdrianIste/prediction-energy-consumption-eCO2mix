"""Data shown on the monitoring dashboard."""

import pandas as pd

from load_forecast.db import read_sql

DAY_AHEAD = "target_day = issued_on + 1"


def load_latest_forecast() -> pd.DataFrame:
    """Return the 48 half-hours of the most recent day-ahead forecast."""
    return read_sql(
        """
        SELECT ts, forecast_mw
        FROM forecasts
        WHERE issued_on = (SELECT max(issued_on) FROM forecasts)
          AND (ts AT TIME ZONE 'Europe/Paris')::date = issued_on + 1
        ORDER BY ts
        """
    )


def load_recent_comparison(days: int = 14) -> pd.DataFrame:
    """Return forecast and actual consumption over the last days."""
    return read_sql(
        f"""
        SELECT ts, forecast_mw, actual_mw
        FROM forecast_errors
        WHERE {DAY_AHEAD}
          AND target_day >= current_date - %s
        ORDER BY ts
        """,
        (days,),
    )


def load_daily_errors() -> pd.DataFrame:
    """Return the MAPE of the model and of RTE for each target day."""
    return read_sql(
        f"""
        SELECT
            target_day,
            avg(abs_pct_error) AS model_mape_pct,
            avg(abs(rte_forecast_mw - actual_mw)::float / actual_mw * 100) AS rte_mape_pct
        FROM forecast_errors
        WHERE {DAY_AHEAD}
        GROUP BY target_day
        ORDER BY target_day
        """
    )
