# activesg-gym-scrapper

Python scraper for ActiveSG gym capacity and Singapore weather data. The scraper uses Selenium for ActiveSG gym capacity, Data.gov.sg APIs for weather data, and PostgreSQL for storage.

## Requirements

- Python 3.13, managed with `uv`
- Docker or Docker Compose for the local PostgreSQL database
- Chromium or Chrome plus a compatible driver for Selenium
- Xvfb on Raspberry Pi or other headless Linux hosts

Install `uv` if it is not already available:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Raspberry Pi or headless Linux setup:

```bash
sudo apt-get install chromium-browser xvfb
chromium-browser --version
```

## Setup

Install Python dependencies from the repository root:

```bash
uv sync
```

This creates `.venv` and installs dependencies from `pyproject.toml` and `uv.lock`.

Start the local PostgreSQL database:

```bash
cd project
docker compose up
```

The compose file uses local development credentials and initializes the database from `project/database/Telemetry.sql`.

## Run

Run the scraper in the foreground from the repository root:

```bash
uv run python project/src/main.py
```

Or use the restart script:

```bash
./project/run.sh
```

The script stops any matching running scraper process, restarts it with `uv run`, and writes logs to `project/src/run.log`.

## Development

Run Ruff lint checks:

```bash
uv run ruff check project/src
```

Format source files:

```bash
uv run ruff format project/src
```

Run a quick syntax check:

```bash
uv run python -m compileall project/src
```

Tests are not yet committed. Add future tests under `project/tests` and run them with:

```bash
uv run pytest
```

## Project Layout

- `project/src/main.py`: application entry point
- `project/src/worker/`: scraping loop and orchestration
- `project/src/controller/`: gym capacity and weather data processing
- `project/src/web/`: Selenium scraper
- `project/src/httprequests/`: Data.gov.sg HTTP client
- `project/src/database/` and `project/src/model/`: SQLAlchemy tables and database access
- `project/src/assets/`: static gym address and SportSG GeoJSON data
