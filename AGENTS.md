# Repository Guidelines

## Project Structure & Module Organization

This repository contains a Python scraper for ActiveSG gym capacity data. Runtime code lives in `project/src`, with `main.py` starting `worker.ScrapingThread`. Major modules are grouped by role: `controller/` fetches gym and weather data, `web/` handles Selenium scraping, `database/` and `model/` wrap SQLAlchemy access, `logger/` centralizes logging, and `error/` defines custom errors. Static files are in `project/src/assets`. Dependency metadata is in `pyproject.toml`; Postgres setup is in `project/docker-compose.yml` and `project/database/Telemetry.sql`.

## Build, Test, and Development Commands

- `uv sync`: create `.venv` and install runtime dependencies from `pyproject.toml`.
- `cd project && docker compose up`: start the local Postgres database using the bundled schema.
- `uv run python project/src/main.py`: run the scraper in the foreground for local debugging.
- `./project/run.sh`: stop any matching existing scraper process and restart it with `uv run` and `nohup`, writing `project/src/run.log`.
- `uv run pytest`: run tests with coverage reporting and the 80% coverage gate.
- `uv run ruff check project/src project/tests`: run lint checks, including PEP 8 naming rules.
- `uv run ruff format project/src project/tests`: format Python files with Ruff.

On Linux hosts, install Chromium, a compatible driver, and Xvfb before Selenium scraping.

## Coding Style & Naming Conventions

Use Python 3.13 and follow PEP 8. Classes use CapWords, such as `GymCapacity`, `Database`, and `ScrapingThread`; functions, variables, modules, and files use `snake_case`, such as `get_data`, `query_one`, and `send_request.py`. Keep imports grouped near the top, except for script-mode path bootstraps allowed by Ruff `E402` ignores. Route diagnostics through `logger.logger`.

## Testing Guidelines

Tests live under `project/tests` and use `pytest` plus `pytest-cov`. Name files `test_<module>.py`, mock external services with `MagicMock` or fakes, and preserve at least 80% total coverage. Current tests cover request parsing, weather matching, database helpers, services, gym enrichment, and Selenium parsing. For runtime verification, start Postgres with Docker and run `uv run python project/src/main.py`.

## Commit & Pull Request Guidelines

Recent commits use short bracketed prefixes such as `[Add]`, `[Fix]`, `[Fixed]`, `[Remove]`, and `[Issue]`. Continue that pattern, for example `[Fix] - handle empty gym capacity response`. Pull requests should describe changes, verification steps, database or environment changes, and scraper output logs when relevant.

## Security & Configuration Tips

Do not commit real credentials, browser binaries, generated logs, or local database volumes. Docker Compose uses test Postgres credentials for local development only. Keep host-specific paths out of source files, and document required setup changes in `README.md`.
