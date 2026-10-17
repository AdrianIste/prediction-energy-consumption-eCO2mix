# Data exploration

Summary of the exploration notebooks and of the decisions they lead to
for the modelling step. Details and charts are in the notebooks.

| Notebook | Content |
| [01_first_look](../notebooks/01_first_look.ipynb) | First look at the dataset and visualization of the RTE forecast |
| [02_data_quality](../notebooks/02_data_quality.ipynb) | Gaps, missing values, extreme values |
| [03_consumption_patterns](../notebooks/03_consumption_patterns.ipynb) | Daily, weekly and yearly cycles, public holidays |
| [04_temperature](../notebooks/04_temperature.ipynb) | Relationship between consumption and temperature |

## Data quality

- Two half-hours are missing every year from 2012 to 2025, on the last
  Sunday of October around 02:00 Paris time: the autumn daylight saving
  time change.
- One consumption value is missing on 1 January 2026 at 00:00 Paris
  time, at the boundary between final and consolidated data (hypothesis:
  a joining defect between two batches of RTE data).
- No temperature is missing. Extreme values are plausible in both
  tables.

## Consumption patterns

- Daily cycle: consumption is lowest around 5:00 and highest around 1:00 and 20:00
  (Paris time). Weekends are lower.
- Weekly cycle: working days are similar; Saturdays are lower and
  Sundays the lowest.
- Yearly cycle: highest in January, lowest in August, about 20000 MW apart.
- Public holidays on weekdays behave like Sundays.

## Temperature

- Below about 16 °C, consumption increases by about 2300 MW per degree
  colder, because of electric heating.
- Between about 16 °C and 25 °C, temperature has little effect; above,
  consumption rises slightly with air conditioning.
- Colder years have higher consumption; 2013 was both the coldest year
  and the one with the highest consumption.

## Decisions for the model

| Finding | Decision for the modelling step |
| --- | --- |
| Missing half-hours and values | Excluded from training, not filled |
| Daily cycle | Feature: half-hour of the day, in Paris time |
| Weekly cycle | Feature: day of the week |
| Public holidays behave like Sundays | Feature: public holiday flag |
| Hockey-stick relationship with temperature | Features: national temperature and heating degrees|
| Simple average of ten cities | Test a population-weighted national temperature |
| Long-term decline | Check whether training on recent years only gives better forecasts |
| Weather is hourly, consumption half-hourly | Interpolate temperature to half-hours |
