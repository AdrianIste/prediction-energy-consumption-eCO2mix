"""Baseline forecasts used as references for the models."""

import pandas as pd

from load_forecast.evaluation.protocol import PARIS_TZ

MIN_LAG_DAYS = 2


def seasonal_naive(consumption: pd.Series, slots: pd.DatetimeIndex, days: int = 7) -> pd.Series:
    """Forecast each half-hour with the value at the same Paris time, days earlier."""
    if days < MIN_LAG_DAYS:
        raise ValueError(f"A lag of {days} days uses data not available at noon.")
    local_times = slots.tz_convert(PARIS_TZ).tz_localize(None)
    lagged_local = local_times - pd.Timedelta(days=days)
    lagged = lagged_local.tz_localize(PARIS_TZ, ambiguous="NaT", nonexistent="NaT").tz_convert(
        "UTC"
    )
    values = consumption.reindex(lagged).to_numpy()
    return pd.Series(values, index=slots, name="forecast_mw")
