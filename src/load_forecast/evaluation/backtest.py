"""Run a forecasting method over target days and collect forecasts with actuals."""

import datetime as dt
from collections.abc import Callable

import pandas as pd

from load_forecast.evaluation.protocol import half_hours, prediction_time
from load_forecast.metrics import mae, mape


def build_forecasts(
    forecast_fn: Callable[[pd.DatetimeIndex], pd.Series],
    actual: pd.Series,
    days: list[dt.date],
) -> pd.DataFrame:
    """Forecast every target day and return one row per half-hour."""
    frames = []
    for day in days:
        slots = half_hours(day)
        horizon = slots - prediction_time(day)
        frame = pd.DataFrame(
            {
                "target_day": day,
                "forecast_mw": forecast_fn(slots).to_numpy(),
                "actual_mw": actual.reindex(slots).to_numpy(),
                "horizon_h": horizon.total_seconds().to_numpy() / 3600,
            },
            index=slots,
        )
        frames.append(frame)
    return pd.concat(frames)


def summarize(forecasts: pd.DataFrame, by: str | None = None) -> pd.DataFrame:
    """Return MAE (MW) and MAPE (%) overall or per group, ignoring missing values."""
    valid = forecasts.dropna(subset=["forecast_mw", "actual_mw"])

    def scores(group: pd.DataFrame) -> pd.Series:
        return pd.Series(
            {
                "mae_mw": mae(group["actual_mw"], group["forecast_mw"]),
                "mape_pct": mape(group["actual_mw"], group["forecast_mw"]),
            }
        )

    if by is None:
        return scores(valid).to_frame().T
    if by == "month":
        key = pd.to_datetime(valid["target_day"]).dt.month
    else:
        key = valid[by]
    return valid.groupby(key)[["actual_mw", "forecast_mw"]].apply(scores)
