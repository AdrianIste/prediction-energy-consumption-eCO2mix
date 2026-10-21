.PHONY: install lint format test check db-up db-down db-init db-shell download load ingest train predict api up daily

install:
	uv sync
	uv run pre-commit install

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

check: lint test

db-up:
	docker compose up -d --wait db
db-down:
	docker compose down

db-init:
	docker compose exec -T db psql -U load_forecast -d load_forecast < sql/001_create_consumption.sql
	docker compose exec -T db psql -U load_forecast -d load_forecast < sql/002_create_consumption_realtime.sql
	docker compose exec -T db psql -U load_forecast -d load_forecast < sql/003_create_weather.sql
	docker compose exec -T db psql -U load_forecast -d load_forecast < sql/004_create_weather_forecast.sql
	docker compose exec -T db psql -U load_forecast -d load_forecast < sql/005_create_weather_forecast_daily.sql
	docker compose exec -T db psql -U load_forecast -d load_forecast < sql/006_create_forecasts.sql
	docker compose exec -T db psql -U load_forecast -d load_forecast < sql/007_create_forecast_errors.sql

db-shell:
	docker compose exec db psql -U load_forecast -d load_forecast

download:
	uv run python -m load_forecast.ingest.eco2mix
	uv run python -m load_forecast.ingest.open_meteo
	uv run python -m load_forecast.ingest.open_meteo_forecast


load:
	uv run python -m load_forecast.ingest.load_consumption
	uv run python -m load_forecast.ingest.load_weather
	uv run python -m load_forecast.ingest.load_weather_forecast
ingest: db-up db-init download load

train:
	uv run python -m load_forecast.training
predict:
	uv run python -m load_forecast.predict --day $(DAY)
api:
	uv run uvicorn load_forecast.api:app --reload
up:
	docker compose up --build
daily: db-up
	uv run python -m load_forecast.ingest.eco2mix
	uv run python -m load_forecast.ingest.load_consumption
	uv run python -m load_forecast.ingest.open_meteo_daily
	uv run python -m load_forecast.daily
