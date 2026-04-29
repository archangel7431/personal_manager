# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

```bash
uv sync
```

This creates `.venv` and installs all dependencies from `uv.lock`. Add new dependencies via `uv add <package>`.

## Running the App

Run the budgeting module directly (must be run from the repo root so `logging_config.yaml` is resolvable):
```bash
uv run python -m personal_manager.budgeting.app
```

## Running Tests

Run all tests from the repo root:
```bash
uv run python -m unittest discover -s personal_manager -p "utils_test.py"
```

Run a single test class:
```bash
uv run python -m unittest personal_manager.budgeting.utils_test.TestBudget
```

Run a single test method:
```bash
uv run python -m unittest personal_manager.budgeting.utils_test.TestBudget.test_expense_entry
```

## Architecture

The repo is structured as a personal manager app where each feature lives in its own sub-package under `personal_manager/`. Currently only the `budgeting` sub-package exists.

**Key structural rules (from `idea.md`):**
- Each feature is a separate folder/module with its own `__init__.py` and a `documentation_trial.md`
- Build prototypes first, then iterate

**Logging** is configured globally via `logging_config.yaml` (repo root) and loaded through `logging_config.py`. Every sub-package imports `setup_logging()` and creates a `logger = logging.getLogger(__name__)` in its `__init__.py`. The `logging_config.yaml` must be present in the working directory at runtime (i.e., run from repo root).

**Budgeting sub-package** (`personal_manager/budgeting/`):
- `__init__.py` — sets up logging and exposes `expense_entry`
- `utils_expense_entry.py` — all business logic: directory/file setup, CSV append, interactive user input loop, daily scheduling via `schedule`
- `app.py` — entry point; instantiates `Budget` and calls `add_expense()`
- Data is stored as CSV at `personal_manager/budgeting/data/budget.csv` with columns `Date, Section_name, Section_value`

**CSV header contract:** `["Date", "Section_name", "Section_value"]` — `checking_for_file` enforces this and backs up the old file if headers mismatch.
