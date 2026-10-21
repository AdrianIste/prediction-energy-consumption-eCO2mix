import pandas as pd

from load_forecast.model import train_model
from load_forecast.predict import load_model


def test_saved_model_gives_the_same_predictions(tmp_path):
    X = pd.DataFrame({"a": range(100), "b": range(100, 200)}, dtype=float)
    y = pd.Series(range(100), dtype=float)
    model = train_model(X, y, n_estimators=10)

    path = tmp_path / "model.json"
    model.save_model(path)
    reloaded = load_model(path)

    assert (reloaded.predict(X) == model.predict(X)).all()
