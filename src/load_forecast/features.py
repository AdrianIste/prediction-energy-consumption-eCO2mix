"""Build the input features of the models for a set of half-hours."""

import holidays
import pandas as pd

from load_forecast.evaluation.protocol import PARIS_TZ

HEATING_THRESHOLD_C = 16


def build_features(slots: pd.DatetimeIndex, temperature: pd.Series) -> pd.DataFrame:
    """Return one row per half-hour with calendar and temperature features."""
    paris = slots.tz_convert(PARIS_TZ)
    slot_of_day = paris.hour * 2 + paris.minute // 30
    features = pd.DataFrame(index=slots)
    for slot in range(48):
        features[f"slot_{slot}"] = (slot_of_day == slot).astype(int)
    for day in range(7):
        features[f"weekday_{day}"] = (paris.dayofweek == day).astype(int)
    years = range(paris.year.min(), paris.year.max() + 1)
    fr_holidays = holidays.France(years=years)
    features["is_holiday"] = pd.Index(paris.date).isin(list(fr_holidays)).astype(int)
    half_hourly = temperature.resample("30min").interpolate()
    features["temperature_c"] = half_hourly.reindex(slots).to_numpy()
    heating = HEATING_THRESHOLD_C - features["temperature_c"]
    features["heating_degrees"] = heating.clip(lower=0)
    return features
