CREATE TABLE IF NOT EXISTS consumption_realtime (
    ts              TIMESTAMPTZ NOT NULL,
    consumption_mw  INTEGER,
    forecast_d1_mw  INTEGER,
    archived_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (ts)
);
