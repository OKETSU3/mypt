#SetUp
#Sync
sync:
		uv sync --all-extras

#Tests
test:
		uv run pytest

test-cov:
		uv run pytest --cov=src --cov-report=term-missing --cov-report=html

test-unit:
		uv run pytest tests/unit -v

test-property:
		uv run pytest tests/property -v

test-integration:
		uv run pytest tests/integration -v

#Formatting
format:
		uv run ruff format . --config=pyproject.toml

#Linting
lint:
		uv run ruff check . --fix --config=pyproject.toml

#Type Checking
type-check:
		uv run pyright

#Security
security:
		uv run bandit -c pyproject.toml -r src

#Audit
audit:
		uv run pip-audit