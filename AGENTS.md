# Repository Guidelines

## Project Structure & Module Organization

This repository contains a Python scraper for ActiveSG gym capacity data. Runtime code lives in `project/src`, with `main.py` starting `worker.ScrapingThread`. Major modules are grouped by role: `controller/` fetches gym capacity and weather data, `web/` handles Selenium scraping, `database/` and `model/` wrap SQLAlchemy access, `logger/` centralizes logging, and `error/` defines custom errors. Static input files are in `project/src/assets`. Dependency metadata is in `pyproject.toml`; Postgres setup is in `project/docker-compose.yml` and `project/database/Telemetry.sql`.

## Build, Test, and Development Commands

- `uv sync`: create `.venv` and install runtime dependencies from `pyproject.toml`.
- `cd project && docker compose up`: start the local Postgres database using the bundled schema.
- `uv run python project/src/main.py`: run the scraper in the foreground for local debugging.
- `./project/run.sh`: stop any matching existing scraper process and restart it with `uv run` and `nohup`, writing `project/src/run.log`.
- `uv run ruff check project/src`: run lint checks, including PEP 8 naming rules.
- `uv run ruff format project/src`: format Python files with Ruff.

On Raspberry Pi or Linux hosts, install Chromium, a compatible driver, and Xvfb before Selenium scraping.

## Coding Style & Naming Conventions

Use Python 3.13 and follow PEP 8. Classes use CapWords, such as `GymCapacity`, `Database`, and `ScrapingThread`; functions, methods, variables, modules, and files use `snake_case`, such as `get_data`, `query_one`, and `send_request.py`. Keep imports grouped near the top, except for the script-mode path bootstrap allowed by Ruff `E402` ignores. Route diagnostics through `logger.logger`.

## Testing Guidelines

There is no committed automated test suite yet. When adding tests, place them under `project/tests` and name files `test_<module>.py`. Prefer `pytest`, especially around parsing, database wrappers, retry behavior, and service transformations. Until tests exist, verify changes manually by starting Postgres with Docker and running `uv run python project/src/main.py`.

## Commit & Pull Request Guidelines

Recent commits use short bracketed prefixes such as `[Add]`, `[Fix]`, `[Fixed]`, `[Remove]`, and `[Issue]`. Continue that pattern, for example `[Fix] - handle empty gym capacity response`. Pull requests should describe behavior changes, verification steps, database or environment changes, and scraper output logs when relevant.

## Security & Configuration Tips

Do not commit real credentials, browser binaries, generated logs, or local database volumes. The Docker Compose file uses test Postgres credentials for local development only. Keep host-specific paths out of source files where possible, and document any required Raspberry Pi setup changes in `README.md`.
