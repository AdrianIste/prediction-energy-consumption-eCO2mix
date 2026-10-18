import datetime as dt

import pandas as pd
import pytest

from load_forecast.evaluation.baselines import seasonal_naive
from load_forecast.evaluation.protocol import half_hours


def make_series(start: str, end: str) -> pd.Series:
    """A fake consumption series: one distinct value per half-hour."""
    index = pd.date_range(start, end, freq="30min", tz="UTC", inclusive="left")
    return pd.Series(range(len(index)), index=index, dtype=float)


def test_forecast_is_the_value_seven_days_earlier():
    consumption = make_series("2025-01-01", "2025-01-20")
    slots = half_hours(dt.date(2025, 1, 15))

    forecast = seasonal_naive(consumption, slots)

    expected = consumption.loc[slots - pd.Timedelta(days=7)].to_numpy()
    assert (forecast.to_numpy() == expected).all()


def test_lag_follows_paris_time_across_daylight_saving_change():
    consumption = make_series("2025-10-15", "2025-10-30")
    slot = pd.DatetimeIndex([pd.Timestamp("2025-10-27 07:00", tz="UTC")])

    forecast = seasonal_naive(consumption, slot)

    assert forecast.iloc[0] == consumption[pd.Timestamp("2025-10-20 06:00", tz="UTC")]


def test_ambiguous_lagged_time_gives_no_forecast():
    consumption = make_series("2025-10-20", "2025-11-05")
    slot = pd.DatetimeIndex([pd.Timestamp("2025-11-02 01:00", tz="UTC")])

    assert seasonal_naive(consumption, slot).isna().all()


def test_lag_shorter_than_two_days_is_refused():
    consumption = make_series("2025-01-01", "2025-01-20")
    with pytest.raises(ValueError):
        seasonal_naive(consumption, half_hours(dt.date(2025, 1, 15)), days=1)
