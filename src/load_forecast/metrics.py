"""forecast error metrics."""

from collections.abc import Sequence

import numpy as np


def mae(actual: Sequence[float], predicted: Sequence[float]) -> float:
    """Mean absolute error, in the unit of the inputs."""
    actual_arr = np.asarray(actual, dtype=float)
    predicted_arr = np.asarray(predicted, dtype=float)
    return float(np.mean(np.abs(actual_arr - predicted_arr)))


def mape(actual: Sequence[float], predicted: Sequence[float]) -> float:
    """Mean absolute percentage error, in percent."""
    actual_arr = np.asarray(actual, dtype=float)
    predicted_arr = np.asarray(predicted, dtype=float)
    return float(np.mean(np.abs(actual_arr - predicted_arr) / actual_arr * 100))
