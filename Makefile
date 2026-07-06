.PHONY: help install install-dev test run-example clean

help:
	@echo "Available commands:"
	@echo "  make install      Install the project in editable mode"
	@echo "  make install-dev  Install the project with development dependencies"
	@echo "  make test         Run the test suite"
	@echo "  make run-example  Run the CLI with an example bug report"
	@echo "  make clean        Remove Python cache and build artifacts"

install:
	python -m pip install -e .

install-dev:
	python -m pip install -e ".[dev]"

test:
	pytest

run-example:
	python main.py "App crashes when I click the login button after entering a valid email."

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov
	rm -f .coverage
	rm -rf build dist *.egg-info
