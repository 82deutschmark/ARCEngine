# Repository Guidelines

## Project Structure & Module Organization

- `arcengine/`: library source (core modules: `base_game.py`, `level.py`, `camera.py`, `sprites.py`, `enums.py`).
- `tests/`: pytest suite (`tests/test_*.py`).
- `examples/`: runnable sample games and utilities (start with `examples/main.py`).
- Top-level config: `pyproject.toml` (dependencies + mypy/ruff), `.pre-commit-config.yaml` (hooks).

## Build, Test, and Development Commands

Assumes an active virtual environment.

- `uv sync`: install/update dev dependencies from `pyproject.toml`/`uv.lock`.
- `pre-commit install`: install git hooks (runs ruff + mypy on commit).
- `pre-commit run --all-files`: run formatting, linting, and type checking locally.
- `python -m pytest`: run the full test suite.
- `python -m pytest tests/test_level.py -v`: run a single file verbosely.

## Coding Style & Naming Conventions

- Python formatting/linting: `ruff` + `ruff-format` via pre-commit.
- Typing: strict `mypy` (tests are excluded from type checking).
- Line length: 280 characters (sprite pixel data often needs wider lines).
- Naming: modules and functions use `snake_case`; types/classes use `PascalCase`.

## Testing Guidelines

- Framework: `pytest`.
- File naming: `tests/test_<module>.py` (e.g., `tests/test_camera.py`).
- Prefer small, deterministic tests for collision logic, rendering, and enum/data-model behavior.

## Commit & Pull Request Guidelines

- Commit messages in this repo trend toward short, imperative summaries (e.g., “Fix …”, “Add …”, “Update …”, “Version bump”).
- Keep commits focused; include a brief rationale in the PR description.
- PRs should include: summary, how to test (commands + expected behavior), and any compatibility notes.

## Engine Constraints (Keep These Intact)

- Output is always a 64×64 grid with a 16-color palette.
- Gameplay is turn-based; each action can emit 1–N frames (hard cap: 1000 frames/action).
- Game subclasses implement `ARCBaseGame.step()` and must call `complete_action()` when input handling finishes.

