# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

```bash
uv sync
```

This creates `.venv` and installs all dependencies from `uv.lock`. Add new dependencies via `uv add <package>`.

Dependencies: `PyYAML==6.0.2`, `schedule==1.2.2`.

## Running the App

Always run from the repo root so `logging.yaml` is resolvable:
```bash
uv run python -m personal_manager.expense_entry_and_tracking.<module>
```

## Running Tests

```bash
uv run python -m unittest discover -s personal_manager -p "*_test.py"
```

Single test class or method:
```bash
uv run python -m unittest personal_manager.<subpackage>.<test_module>.<TestClass>
uv run python -m unittest personal_manager.<subpackage>.<test_module>.<TestClass>.<test_method>
```

**Logging** is configured globally via `logging.yaml` (repo root) and loaded through `logging_config.py`. 
- **`app_errors.log`**: Root log file capturing `ERROR` level and above for the entire application.
- **Dynamic `activity.log`**: Each module automatically gets an `activity.log` file in its own directory capturing `DEBUG` level and above. This is handled by `logging_config.py:setup_logging()` which uses `inspect` to detect the calling module.
- Each `__init__.py` should simply call `setup_logging()` (no arguments needed) to initialize both global and module-specific logging.

**`expense_entry_and_tracking` sub-package** (`personal_manager/expense_entry_and_tracking/`):
- Active development area for expense entry and tracking functionality
- `__init__.py` — sets up logging for the sub-package
- `trial.py` — early prototype: interactive CLI that appends dated expense entries to a flat text file
