CREATE TABLE IF NOT EXISTS weather_forecast (
    city           TEXT  NOT NULL,
    ts             TIMESTAMPTZ NOT NULL,
    temperature_c  DOUBLE PRECISION,
    loaded_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (city, ts)
);
-- Temperature forecast made 48 hours ahead (Open-Meteo previous runs, previous_day2).
