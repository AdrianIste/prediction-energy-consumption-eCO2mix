CREATE TABLE IF NOT EXISTS weather (
    city           TEXT  NOT NULL,
    ts             TIMESTAMPTZ NOT NULL,
    temperature_c  DOUBLE PRECISION,
    loaded_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (city, ts)
);
