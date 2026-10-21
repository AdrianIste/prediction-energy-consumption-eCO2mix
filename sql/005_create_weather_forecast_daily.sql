-- Hourly temperature forecast fetched each morning from the Open-Meteo forecast API.
CREATE TABLE IF NOT EXISTS weather_forecast_daily (
    city           TEXT NOT NULL,
    ts             TIMESTAMPTZ NOT NULL,
    issued_on      DATE NOT NULL,
    temperature_c  DOUBLE PRECISION,
    loaded_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (city, ts, issued_on)
);
