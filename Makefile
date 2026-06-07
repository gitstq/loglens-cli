.PHONY: install dev test lint format clean build run help

help:
	@echo "🎯 LogLens-CLI Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install    Install dependencies"
	@echo "  dev        Install dev dependencies"
	@echo "  test       Run tests"
	@echo "  lint       Run linter"
	@echo "  format     Format code with black"
	@echo "  clean      Clean build artifacts"
	@echo "  build      Build distribution"
	@echo "  run        Run LogLens TUI"

install:
	pip install -r requirements.txt
	pip install -e .

dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=loglens --cov-report=term-missing

lint:
	flake8 loglens/ --max-line-length=100

format:
	black loglens/ tests/ --line-length=100

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

run:
	python -m loglens.cli
