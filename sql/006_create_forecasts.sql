-- Consumption forecasts produced each day by the model.
CREATE TABLE IF NOT EXISTS forecasts (
    ts                TIMESTAMPTZ NOT NULL,
    issued_on         DATE NOT NULL,
    forecast_mw       INTEGER NOT NULL,
    model_trained_at  TIMESTAMPTZ NOT NULL,
    loaded_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (ts, issued_on)
);
