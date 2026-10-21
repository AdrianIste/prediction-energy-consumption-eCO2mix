"""Train the final model from the database, without a notebook."""

import datetime as dt
import json
import logging
from pathlib import Path

from xgboost import XGBRegressor

from load_forecast.evaluation.data import load_actuals, load_temperature
from load_forecast.evaluation.protocol import TEST
from load_forecast.logging_setup import setup_logging
from load_forecast.model import (
    LEARNING_RATE,
    MAX_DEPTH,
    N_ESTIMATORS,
    TRAIN_START,
    build_training_data,
    train_model,
)

logger = logging.getLogger(__name__)

DEFAULT_TRAIN_END = TEST[1]
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "model.json"
METADATA_PATH = MODEL_DIR / "metadata.json"


def train_final_model(end_day: dt.date = DEFAULT_TRAIN_END) -> tuple[XGBRegressor, dict]:
    """Train the final model on all consolidated data from TRAIN_START to end_day."""
    actuals = load_actuals()
    temperature = load_temperature()

    X, y = build_training_data(actuals, temperature, end_day)
    X = X.loc[TRAIN_START:]
    y = y.loc[TRAIN_START:]
    logger.info(f"Training on {len(X)} half-hours, from {X.index[0]} to {X.index[-1]}")

    model = train_model(
        X,
        y,
        n_estimators=N_ESTIMATORS,
        max_depth=MAX_DEPTH,
        learning_rate=LEARNING_RATE,
    )
    logger.info("Model trained")

    metadata = {
        "trained_at": dt.datetime.now(dt.UTC).isoformat(),
        "train_start": TRAIN_START,
        "train_end": end_day.isoformat(),
        "n_rows": len(X),
        "features": list(X.columns),
        "params": {
            "n_estimators": N_ESTIMATORS,
            "max_depth": MAX_DEPTH,
            "learning_rate": LEARNING_RATE,
        },
    }
    return model, metadata


def save_model(model: XGBRegressor, metadata: dict) -> None:
    """Write the model and its metadata to the models directory."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.save_model(MODEL_PATH)
    METADATA_PATH.write_text(json.dumps(metadata, indent=2))
    logger.info(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    setup_logging()
    model, metadata = train_final_model()
    save_model(model, metadata)
