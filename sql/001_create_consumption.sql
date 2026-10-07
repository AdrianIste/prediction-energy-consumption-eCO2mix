CREATE TABLE IF NOT EXISTS consumption (
    ts              TIMESTAMPTZ NOT NULL,
    consumption_mw  INTEGER,
    forecast_d1_mw  INTEGER,
    nature          TEXT NOT NULL,
    loaded_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (ts)
);
