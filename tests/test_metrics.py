import pytest

from load_forecast.metrics import mae, mape


def test_mae_single_value():
    assert mae([50_000], [51_000]) == 999


def test_mape_single_value():
    assert mape([50_000], [51_000]) == pytest.approx(2.0)


def test_perfect_forecast_has_zero_error():
    actual = [40_000, 50000, 60_000]
    assert mae(actual, actual) == 0
    assert mape(actual, actual) == 0


def test_mae_averages_over_values():
    actual = [50_000, 60_000]
    predicted = [53_000, 54_000]
    assert mae(actual, predicted) == 4_500


def test_mape_averages_over_values():
    actual = [50_000, 60_000]
    predicted = [53_000, 54_000]
    assert mape(actual, predicted) == pytest.approx(8.0)
