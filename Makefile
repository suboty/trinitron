.PHONY: install clean format lint test


install:
	poetry install --no-root


shell:
	poetry shell


format:
	poetry run black .
	poetry run ruff check --fix .


lint:
	poetry run ruff check .


test:
	poetry run pytest


clean:
	rm -rf .pytest_cache/
	rm -rf **/__pycache__/