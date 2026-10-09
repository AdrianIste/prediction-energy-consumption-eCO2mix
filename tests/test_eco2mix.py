from load_forecast.ingest.eco2mix import build_export_params, read_raw_csv


def test_params_select_the_four_columns():
    params = build_export_params(2020)
    assert params["select"] == "date_heure,consommation,prevision_j1,nature"


def test_params_cover_exactly_one_year():
    params = build_export_params(2020)
    assert params["where"] == ("date_heure >= date'2020-01-01' and date_heure < date'2021-01-01'")


def test_read_raw_csv_keeps_half_hours_only(tmp_path):
    sample = tmp_path / "sample.csv"
    sample.write_text(
        "date_heure;consommation;prevision_j1;nature\n"
        "2025-01-01T00:00:00+00:00;62493;61100;Données définitives\n"
        "2025-01-01T00:15:00+00:00;;61350;Données définitives\n"
        "2025-01-01T00:30:00+00:00;62242;61600;Données définitives\n"
        "2025-01-01T00:45:00+00:00;;61450;Données définitives\n",
        encoding="utf-8-sig",
    )

    result = read_raw_csv(sample)

    assert list(result.columns) == ["ts", "consumption_mw", "forecast_d1_mw", "nature"]
    assert len(result) == 2
    assert result["consumption_mw"].tolist() == [62493, 62242]
