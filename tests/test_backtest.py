import datetime as dt

import pandas as pd
import pytest

from load_forecast.evaluation.backtest import build_forecasts, summarize


def make_series(start: str, end: str) -> pd.Series:
    index = pd.date_range(start, end, freq="30min", tz="UTC", inclusive="left")
    return pd.Series(range(len(index)), index=index, dtype=float)


def test_build_forecasts_has_one_row_per_half_hour_and_correct_horizons():
    actual = make_series("2025-01-01", "2025-01-20")

    def perfect_forecast(slots: pd.DatetimeIndex) -> pd.Series:
        return actual.reindex(slots)

    days = [dt.date(2025, 1, 15), dt.date(2025, 1, 16)]
    result = build_forecasts(perfect_forecast, actual, days)

    assert len(result) == 96
    assert result["horizon_h"].iloc[0] == 12.0
    assert result["horizon_h"].iloc[47] == 35.5
    assert (result["forecast_mw"] == result["actual_mw"]).all()


def test_summarize_ignores_missing_values():
    forecasts = pd.DataFrame(
        {
            "target_day": [dt.date(2025, 1, 15)] * 3,
            "forecast_mw": [110.0, 180.0, None],
            "actual_mw": [100.0, 200.0, 300.0],
            "horizon_h": [12.0, 12.5, 13.0],
        }
    )

    overall = summarize(forecasts)
    by_horizon = summarize(forecasts, by="horizon_h")

    assert overall["mae_mw"].iloc[0] == 15.0
    assert overall["mape_pct"].iloc[0] == pytest.approx(10.0)
    assert len(by_horizon) == 2
