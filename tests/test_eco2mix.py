from load_forecast.ingest.eco2mix import build_export_params


def test_params_select_the_four_columns():
    params = build_export_params(2020)
    assert params["select"] == "date_heure,consommation,prevision_j1,nature"


def test_params_cover_exactly_one_year():
    params = build_export_params(2020)
    assert params["where"] == ("date_heure >= date'2020-01-01' and date_heure < date'2021-01-01'")
