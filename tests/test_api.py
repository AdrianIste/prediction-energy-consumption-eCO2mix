import pandas as pd
from fastapi.testclient import TestClient

from load_forecast import api

client = TestClient(api.app)


def test_health_says_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_invalid_day_is_refused():
    response = client.get("/forecast", params={"day": "not-a-date"})

    assert response.status_code == 422


def test_forecast_returns_one_entry_per_half_hour(monkeypatch):
    def fake_predict_day(day):
        index = pd.date_range("2026-01-14 23:00", periods=3, freq="30min", tz="UTC")
        return pd.Series([70000.4, 71000.6, 72000.0], index=index, name="forecast_mw")

    monkeypatch.setattr(api, "predict_day", fake_predict_day)

    response = client.get("/forecast", params={"day": "2026-01-15"})
    body = response.json()

    assert response.status_code == 200
    assert body["day"] == "2026-01-15"
    assert body["forecasts"][0] == {"ts": "2026-01-14T23:00:00+00:00", "forecast_mw": 70000}
    assert len(body["forecasts"]) == 3
