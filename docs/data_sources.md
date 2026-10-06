# Data sources

| Field                           | Real-time                | Consolidated and final    |
| ------------------------------- | ------------------------ | ------------------------- |
| Dataset ID                      | eco2mix-national-tr      | eco2mix-national-cons-def |
| License                         | Open License v2.0(Etalab)| Open License v2.0 (Etalab)|
| First date                      | 2026-09-01               | 2012-01-01                |
| Last date                       | 2026-10-06               | 2026-08-31                |
| Time step                       | 30min                    | 30min                     |
| Update frequency                | Hourly                   | Monthly                    |
| Consumption column (name, unit) | "consommation"(MW)         | "consommation"(MW)          |
| Forecast columns                | "prevision_j1"             | "prevision_j1"             |
| Values of the "nature" column   | "Données temps réel"       | "Données définitives"/"Données consolidées"|


Checked on: 2026-10-06
Notes : Since the actualisaton of the consolidated and final dataset is done at the middle of the next month of the prevision, and the actualisaton of the Real-time dataset is done hourly, there is a difference of 1 month and a half between the two datasets.
In the consolidated and final dataset, half of the values of consumption are missing.
