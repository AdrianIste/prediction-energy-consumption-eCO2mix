"""Monitoring dashboard of the daily forecasts."""

import pandas as pd
import streamlit as st

from load_forecast.evaluation.protocol import PARIS_TZ
from load_forecast.monitoring import (
    load_daily_errors,
    load_latest_forecast,
    load_recent_comparison,
)

PRODUCTION_START = "21 October 2026"


def to_paris(frame: pd.DataFrame) -> pd.DataFrame:
    """Index a frame by its half-hours, in Paris time, for the charts."""
    frame["ts"] = pd.to_datetime(frame["ts"], utc=True).dt.tz_convert(PARIS_TZ)
    return frame.set_index("ts")


st.set_page_config(page_title="Load forecast monitoring", layout="wide")
st.title("Load forecast monitoring")
st.caption(
    f"Day-ahead forecast of French electricity consumption. Forecasts before "
    f"{PRODUCTION_START} were reconstructed with the saved model and archived "
    f"weather forecasts made 48 hours ahead."
)

errors = load_daily_errors()


if errors.empty:
    st.info("No forecast can be compared with reality yet.")
else:
    left, right = st.columns(2)
    left.metric("Model MAPE", f"{errors['model_mape_pct'].mean():.2f} %")
    right.metric("RTE MAPE", f"{errors['rte_mape_pct'].mean():.2f} %")

# Block 1: tomorrow
st.subheader("Latest forecast")
latest = to_paris(load_latest_forecast())
st.line_chart(latest["forecast_mw"])

# Block 2: forecast and actual
st.subheader("Forecast and actual consumption, last 14 days")
recent = to_paris(load_recent_comparison())
st.line_chart(recent[["forecast_mw", "actual_mw"]])

# Block 3: daily error
st.subheader("Daily MAPE (%)")
st.line_chart(errors.set_index("target_day")[["model_mape_pct", "rte_mape_pct"]])
