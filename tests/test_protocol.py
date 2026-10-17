import datetime as dt

import pandas as pd

from load_forecast.evaluation.protocol import half_hours, prediction_time, target_days


def test_target_days_include_both_ends():
    days = target_days(dt.date(2025, 9, 1), dt.date(2025, 9, 3))
    assert days == [dt.date(2025, 9, 1), dt.date(2025, 9, 2), dt.date(2025, 9, 3)]


def test_ordinary_day_has_48_half_hours_starting_at_paris_midnight():
    slots = half_hours(dt.date(2025, 1, 15))
    assert len(slots) == 48
    assert slots[0] == pd.Timestamp("2025-01-14 23:00", tz="UTC")


def test_daylight_saving_days_have_46_and_50_half_hours():
    assert len(half_hours(dt.date(2026, 3, 29))) == 46
    assert len(half_hours(dt.date(2025, 10, 26))) == 50


def test_prediction_time_is_noon_paris_the_day_before():
    assert prediction_time(dt.date(2025, 10, 27)) == pd.Timestamp(
        "2025-10-26 12:00", tz="Europe/Paris"
    )
