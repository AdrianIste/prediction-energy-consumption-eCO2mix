# Day-ahead electricity load forecasting in France

Daily pipeline that forecasts French national electricity consumption
for the next day and benchmarks the result against RTE's own forecast.

## Problem
Electricity cannot be stored at scale, so supply and demand must be balanced at every instant. RTE, the French transmission system operator (TSO), must know the day before how much electricity will be needed to schedule the production. If the forecast is too low, power plants must be started at short notice at high cost, and if the forecast is too high, the electricity is sold at a low price or generation must be curtailed.

## Target
French national electricity consumption, in MW, at 30-minute resolution, for calendar day D+1 from 00:00 to 23:30 (Europe/Paris local time), i.e. 48 values per forecast.

## Prediction time
One forecast is produced every day at 12:00 (Europe/Paris local time)
on day D, for day D+1.

Information available at that time:
- Consumption:  measure consumption up to apporximately 11:00 on day D plus the full history.
- Weather: Weather forecast for day D+1.
- Calendar: weekday, public holidays and time of year of day D+1.

Limitation: the time at which RTE produces its own day-ahead forecast
is unknown, so the comparison is not guaranteed to be made with equal
information.

## Metric
- Primary metric: MAPE (Mean Absolute Percentage Error), in %. It is chosen because
  consumption is much higher in winter than in summer, and a relative error
  remains comparable across seasons.
- Secondary metric: MAE (Mean Absolute Error), in MW. It expresses the error
  in the physical unit, which is what an operator has to compensate.

Both are computed over the 48 values of each forecast, then averaged
over all days of the test period.

## Baselines
1. Seasonal naive: the consumption measured at the same half-hour
   7 days before the target time. It needs no training and captures the
   weekly cycle of consumption. A 364-day variant will also be evaluated.
2. RTE day-ahead forecast: the forecast published by RTE the day
   before, available in the éCO2mix data (column `prevision_j1`). It is the
   reference of the industry.

The first one is the minimum to beat; the second one is the target
to approach.

## Success criteria
Evaluated on the test period (2025-09-01 to 2026-08-31), never used for training:
- Minimum: MAPE lower than the seasonal naive baseline.
- Reported: the gap between the model's MAPE and that of the RTE
  day-ahead forecast.
The daily forecast runs without manual action, and a
third party can reproduce the results from this repository.

## Out of scope
- Regional forecasts: only the national level is covered.
- Other horizons: no intraday or week-ahead forecast.
- Other quantities: no forecast of generation, prices or CO2 emissions.

## Data sources

| Source | Content | License |
| --- | --- | --- |
| [éCO2mix real-time](https://odre.opendatasoft.com/explore/dataset/eco2mix-national-tr/) | National consumption and RTE forecasts, recent weeks, 15-minute step, provisional values | Open License v2.0 (Etalab)|
| [éCO2mix consolidated and final](https://odre.opendatasoft.com/explore/dataset/eco2mix-national-cons-def/) | National consumption and RTE forecasts, 2012 to last month, 30-minute step, consolidated then final values | Open License v2.0 (Etalab) |
| [Open-Meteo](https://open-meteo.com/) | Hourly weather forecasts and historical weather | CC BY 4.0 |

Details in [data source notes](docs/data_sources.md).
