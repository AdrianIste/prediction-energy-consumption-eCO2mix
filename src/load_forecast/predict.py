"""Load the trained model and forecast a target day, without retraining."""

import argparse
import datetime as dt
import json
import logging
from pathlib import Path

import pandas as pd
from xgboost import XGBRegressor

from load_forecast.db import connect
from load_forecast.evaluation.data import load_actuals, load_temperature_forecast
from load_forecast.evaluation.protocol import half_hours
from load_forecast.logging_setup import setup_logging
from load_forecast.model import make_forecast_fn
from load_forecast.training import METADATA_PATH, MODEL_PATH

logger = logging.getLogger(__name__)


def load_model(path: Path = MODEL_PATH) -> XGBRegressor:
    """Read the model saved by make train."""
    model = XGBRegressor()
    model.load_model(path)
    return model


def predict_day(day: dt.date, temperature: pd.Series | None = None) -> pd.Series:
    """Forecast the half-hours of a Paris calendar day with the saved model.

    By default, uses the archived temperature forecast made 48 hours ahead.
    """
    if temperature is None:
        temperature = load_temperature_forecast()
    model = load_model()
    actuals = load_actuals()
    forecast = make_forecast_fn(model, temperature, actuals["consumption_mw"])
    return forecast(half_hours(day))


SAVE_SQL = """
    INSERT INTO forecasts (ts, issued_on, forecast_mw, model_trained_at)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (ts, issued_on) DO UPDATE SET
        forecast_mw = EXCLUDED.forecast_mw,
        model_trained_at = EXCLUDED.model_trained_at,
        loaded_at = now()
"""


def save_forecast(prediction: pd.Series, issued_on: dt.date) -> int:
    """Store a day of forecasts, tagged with the issue day and the model version."""
    metadata = json.loads(METADATA_PATH.read_text())
    trained_at = metadata["trained_at"]
    rows = [(ts, issued_on, round(value), trained_at) for ts, value in prediction.items()]
    with connect() as conn, conn.cursor() as cursor:
        cursor.executemany(SAVE_SQL, rows)
    logger.info(f"Saved {len(rows)} forecasts issued on {issued_on}")
    return len(rows)


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(description="Forecast a target day.")
    parser.add_argument("--day", required=True, help="Target day, as YYYY-MM-DD")
    args = parser.parse_args()

    day = dt.date.fromisoformat(args.day)
    prediction = predict_day(day)
    logger.info(f"Forecast for {day}: {len(prediction)} half-hours")
    print(prediction.round(0).to_string())
