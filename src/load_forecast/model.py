import datetime as dt

import pandas as pd
from xgboost import XGBRegressor

from load_forecast.evaluation.protocol import half_hours
from load_forecast.features import build_features

TRAIN_START = "2021-01-01"
N_ESTIMATORS = 600
MAX_DEPTH = 4
LEARNING_RATE = 0.1


def build_training_data(
    actuals: pd.DataFrame, temperature: pd.Series, end_day: dt.date
) -> tuple[pd.DataFrame, pd.Series]:
    """Return the features and the consumption of every half-hour up to end_day."""

    last_train_slot = half_hours(end_day)[-1]
    y_train = actuals["consumption_mw"].loc[:last_train_slot].dropna()
    X_train = build_features(y_train.index, temperature, y_train)
    has_temperature = X_train["temperature_c"].notna()
    X_train = X_train[has_temperature]
    y_train = y_train[has_temperature]
    return X_train, y_train


def train_model(
    X: pd.DataFrame,
    y: pd.Series,
    n_estimators: int = 100,
    max_depth: int = 6,
    learning_rate: int = 0.3,
) -> XGBRegressor:
    """Train a gradient boosting model on the features and the consumption."""
    model = XGBRegressor(
        random_state=0, n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate
    )
    model.fit(X, y)
    return model


def make_forecast_fn(model: XGBRegressor, temperature: pd.Series, consumption: pd.Series):
    """Return a function that forecasts the given half-hours with the model."""

    def forecast(slots: pd.DatetimeIndex) -> pd.Series:
        features = build_features(slots, temperature, consumption)
        features = features[
            model.feature_names_in_
        ]  # to keep the features the model has trained on
        values = model.predict(features)
        return pd.Series(values, index=slots, name="forecast_mw")

    return forecast
