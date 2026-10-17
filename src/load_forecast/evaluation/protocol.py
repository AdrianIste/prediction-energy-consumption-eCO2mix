"""Evaluation protocol: periods, target days and prediction time."""

import datetime as dt

import pandas as pd

PARIS_TZ = "Europe/Paris"

TRAIN_END = dt.date(2024, 8, 31)
VALIDATION = (dt.date(2024, 9, 1), dt.date(2025, 8, 31))
TEST = (dt.date(2025, 9, 1), dt.date(2026, 8, 31))


def target_days(start: dt.date, end: dt.date) -> list[dt.date]:
    """Return every day from start to end, both included."""
    n_days = (end - start).days + 1
    return [start + dt.timedelta(days=i) for i in range(n_days)]


def half_hours(day: dt.date) -> pd.DatetimeIndex:
    """Return the half-hours of a Paris calendar day, as UTC timestamps."""
    start = pd.Timestamp(day).tz_localize(PARIS_TZ)
    end = pd.Timestamp(day + dt.timedelta(days=1)).tz_localize(PARIS_TZ)
    slots = pd.date_range(start, end, freq="30min", inclusive="left")
    return slots.tz_convert("UTC")


def prediction_time(day: dt.date) -> pd.Timestamp:
    """Return when the forecast for a target day is made: noon, Paris time, the day before."""
    previous_day = day - dt.timedelta(days=1)
    noon = dt.datetime.combine(previous_day, dt.time(12))
    return pd.Timestamp(noon).tz_localize(PARIS_TZ)
