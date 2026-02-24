.PHONY: help test lint format fix security all clean

PYTHON  := python
PACKAGE := rectangles

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  test      Run tests with coverage report"
	@echo "  lint      Run ruff (style) and mypy (types)"
	@echo "  format    Auto-format code with ruff formatter"
	@echo "  fix       Auto-fix ruff lint violations where safe"
	@echo "  security  Run bandit (code) and pip-audit (dependencies)"
	@echo "  all       Run test + lint + security"
	@echo "  clean     Remove generated artefacts"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy $(PACKAGE)

format:
	$(PYTHON) -m ruff format .

fix:
	$(PYTHON) -m ruff check --fix .

security:
	$(PYTHON) -m bandit -r $(PACKAGE) -q
	$(PYTHON) -m pip_audit -r requirements.txt

all: test lint security

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
