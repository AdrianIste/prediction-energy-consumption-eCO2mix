"""Load the trained model and forecast a target day, without retraining."""

import argparse
import datetime as dt
import logging
from pathlib import Path

import pandas as pd
from xgboost import XGBRegressor

from load_forecast.evaluation.data import load_actuals, load_temperature_forecast
from load_forecast.evaluation.protocol import half_hours
from load_forecast.logging_setup import setup_logging
from load_forecast.model import make_forecast_fn
from load_forecast.training import MODEL_PATH

logger = logging.getLogger(__name__)


def load_model(path: Path = MODEL_PATH) -> XGBRegressor:
    """Read the model saved by make train."""
    model = XGBRegressor()
    model.load_model(path)
    return model


def predict_day(day: dt.date) -> pd.Series:
    """Forecast the half-hours of a Paris calendar day with the saved model."""
    model = load_model()
    actuals = load_actuals()
    temperature_forecast = load_temperature_forecast()
    forecast = make_forecast_fn(model, temperature_forecast, actuals["consumption_mw"])
    return forecast(half_hours(day))


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(description="Forecast a target day.")
    parser.add_argument("--day", required=True, help="Target day, as YYYY-MM-DD")
    args = parser.parse_args()

    day = dt.date.fromisoformat(args.day)
    prediction = predict_day(day)
    logger.info(f"Forecast for {day}: {len(prediction)} half-hours")
    print(prediction.round(0).to_string())
