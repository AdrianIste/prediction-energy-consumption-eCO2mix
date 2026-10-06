.PHONY: install lint format test check

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
