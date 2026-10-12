import pandas as pd

from load_forecast.ingest.load_consumption import to_rows


def test_to_rows_replaces_missing_values_with_none():
    frame = pd.DataFrame({"consumption_mw": [62493, None], "nature": ["final", "final"]})
    frame["consumption_mw"] = frame["consumption_mw"].astype("Int64")

    rows = to_rows(frame)

    assert rows == [(62493, "final"), (None, "final")]
