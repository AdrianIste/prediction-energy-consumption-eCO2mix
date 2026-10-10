.PHONY: install lint format test check db-up db-down db-init db-down download load

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
	docker compose up -d

db-down:
	docker compose down

db-init:
	docker compose exec -T db psql -U load_forecast -d load_forecast < sql/001_create_consumption.sql
	docker compose exec -T db psql -U load_forecast -d load_forecast < sql/002_create_consumption_realtime.sql
db-shell:
	docker compose exec db psql -U load_forecast -d load_forecast

download:
	uv run python -m load_forecast.ingest.eco2mix
load:
	uv run python -m load_forecast.ingest.load_consumption
