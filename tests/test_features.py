import datetime as dt

import pandas as pd

from load_forecast.evaluation.protocol import half_hours
from load_forecast.features import build_features


def flat_temperature(day: dt.date, value: float) -> pd.Series:
    """A fake hourly temperature, constant around the given day."""
    start = pd.Timestamp(day) - pd.Timedelta(days=1)
    index = pd.date_range(start, periods=72, freq="h", tz="UTC")
    return pd.Series(value, index=index)


def flat_consumption(day: dt.date, value: float) -> pd.Series:
    """A fake half-hourly consumption, constant over the ten days before the given day."""
    start = pd.Timestamp(day) - pd.Timedelta(days=10)
    index = pd.date_range(start, periods=12 * 48, freq="30min", tz="UTC")
    return pd.Series(value, index=index)


def test_calendar_columns_give_the_half_hour_and_the_weekday():
    day = dt.date(2025, 1, 15)
    features = build_features(
        half_hours(day), flat_temperature(day, 10.0), flat_consumption(day, 50000.0)
    )

    assert features.shape == (48, 6)
    assert features["slot_of_day"].tolist() == list(range(48))
    assert (features["weekday"] == 2).all()


def test_public_holiday_is_flagged():
    may_day = dt.date(2025, 5, 1)
    ordinary_day = dt.date(2025, 5, 7)

    holiday = build_features(
        half_hours(may_day), flat_temperature(may_day, 15.0), flat_consumption(may_day, 50000.0)
    )
    ordinary = build_features(
        half_hours(ordinary_day),
        flat_temperature(ordinary_day, 15.0),
        flat_consumption(ordinary_day, 50000.0),
    )

    assert (holiday["is_holiday"] == 1).all()
    assert (ordinary["is_holiday"] == 0).all()


def test_temperature_is_interpolated():
    temperature = pd.Series(
        [10.0, 12.0, 20.0],
        index=pd.date_range("2025-01-14 23:00", periods=3, freq="h", tz="UTC"),
    )
    slots = pd.date_range("2025-01-14 23:00", periods=5, freq="30min", tz="UTC")

    features = build_features(slots, temperature, flat_consumption(dt.date(2025, 1, 15), 50000.0))
    assert features["temperature_c"].tolist() == [10.0, 11.0, 12.0, 16.0, 20.0]
