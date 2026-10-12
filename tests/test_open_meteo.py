import json

from load_forecast.ingest.open_meteo import read_raw_json


def test_read_raw_json_shapes_rows_like_the_table(tmp_path):
    sample = tmp_path / "paris_2025.json"
    sample.write_text(
        json.dumps(
            {
                "hourly": {
                    "time": ["2025-01-01T00:00", "2025-01-01T01:00"],
                    "temperature_2m": [4.6, 4.8],
                }
            }
        )
    )

    result = read_raw_json("paris", sample)

    assert list(result.columns) == ["city", "ts", "temperature_c"]
    assert result["city"].tolist() == ["paris", "paris"]
    assert result["temperature_c"].tolist() == [4.6, 4.8]
    assert str(result["ts"].iloc[0]) == "2025-01-01 00:00:00+00:00"
