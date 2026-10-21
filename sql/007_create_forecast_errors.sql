-- Error of each stored forecast, once the actual consumption is known.
CREATE OR REPLACE VIEW forecast_errors AS
SELECT
    f.ts,
    f.issued_on,
    f.forecast_mw,
    c.consumption_mw AS actual_mw,
    f.forecast_mw - c.consumption_mw AS error_mw,
    abs(f.forecast_mw - c.consumption_mw)::float / c.consumption_mw * 100 AS abs_pct_error,
    (f.ts AT TIME ZONE 'Europe/Paris')::date AS target_day

FROM forecasts AS f
JOIN consumption AS c ON c.ts = f.ts
WHERE c.consumption_mw IS NOT NULL;
