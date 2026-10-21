"""Forecast tomorrow with today's weather forecast, and store the result."""

import datetime as dt
import logging

from load_forecast.evaluation.data import load_temperature_daily
from load_forecast.logging_setup import setup_logging
from load_forecast.predict import predict_day, save_forecast

logger = logging.getLogger(__name__)


def forecast_tomorrow(today: dt.date | None = None) -> int:
    """Forecast the day after today and store the forecasts."""
    today = today or dt.date.today()
    tomorrow = today + dt.timedelta(days=1)
    temperature = load_temperature_daily(today)
    prediction = predict_day(tomorrow, temperature)
    logger.info(f"Forecast for {tomorrow}: {len(prediction)} half-hours")
    return save_forecast(prediction, today)


if __name__ == "__main__":
    setup_logging()
    forecast_tomorrow()
