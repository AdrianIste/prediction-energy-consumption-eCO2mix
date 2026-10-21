"""Web API that serves the consumption forecast."""

import datetime as dt

from fastapi import FastAPI

from load_forecast.predict import predict_day

app = FastAPI(title="Load forecast API")


@app.get("/health")
def health() -> dict:
    """Tell that the API is running."""
    return {"status": "ok"}


@app.get("/forecast")
def forecast(day: dt.date) -> dict:
    """Return the 48 half-hourly forecasts of a Paris calendar day."""
    prediction = predict_day(day)
    return {
        "day": day.isoformat(),
        "forecasts": [
            {"ts": ts.isoformat(), "forecast_mw": round(value)} for ts, value in prediction.items()
        ],
    }
