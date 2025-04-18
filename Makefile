.PHONY: fmt
fmt:
	@echo "Formatting the code..."
	poetry run ruff format
	poetry run ruff check

.PHONY: lint
lint:
	@echo "Linting the code..."
	poetry run ruff format --check
	poetry run ruff check --no-fix --show-fixes
	poetry run mypy .
