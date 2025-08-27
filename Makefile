.PHONY: help setup format lint typecheck test migrate import-guides run clean build build-exe distclean

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup:  ## Install development dependencies
	pip install -U pip
	pip install -e .[dev]

format:  ## Format code with black
	black .

lint:  ## Lint code with ruff
	ruff check .

typecheck:  ## Type check with mypy
	mypy .

test:  ## Run tests with pytest
	pytest -q --cov=pokemmo_companion --cov-report=term-missing

migrate:  ## Run database migrations
	alembic upgrade head

import-guides:  ## Import guides from JSON files
	python scripts/import_guides.py

run:  ## Run the application
	python -m pokemmo_companion.app

clean:  ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf htmlcov

build:  ## Build the application with PyInstaller
	pyinstaller PokeMMO_Companion.spec --clean

build-exe:  ## Quick build using PyInstaller directly
	pyinstaller --onefile --windowed --name "PokeMMO Companion" \
		--add-data "data:data" \
		--add-data "migrations:migrations" \
		--hidden-import sqlalchemy.sql.default_comparator \
		--hidden-import sqlalchemy.dialects.sqlite \
		--hidden-import alembic \
		--hidden-import pydantic \
		--hidden-import sqlmodel \
		--exclude-module matplotlib \
		--exclude-module numpy \
		--exclude-module pandas \
		--exclude-module scipy \
		--exclude-module tkinter \
		--exclude-module test \
		--exclude-module tests \
		--exclude-module pytest \
		--exclude-module mypy \
		--exclude-module ruff \
		--exclude-module black \
		--exclude-module pre_commit \
		pokemmo_companion/app.py

distclean: clean  ## Clean all build artifacts including PyInstaller
	rm -rf build/
	rm -rf dist/
	rm -rf __pycache__/
	rm -rf pokemmo_companion/__pycache__/
	rm -rf pokemmo_companion/core/__pycache__/
	rm -rf pokemmo_companion/core/services/__pycache__/
	rm -rf pokemmo_companion/ui/__pycache__/
	rm -rf tests/__pycache__/
	rm -f *.spec
