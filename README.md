# activesg-gym-scrapper

Python scraper for ActiveSG gym capacity and weather data.

### raspberry pi
Selenium requires an installed browser that is controlled by a driver. 

```
sudo apt-get install chromium-browser
```

To determine which version you are running:

```
chromium-browser --version
```

Download the prebuilt version from https://github.com/electron/electron/tags 

Install conda https://docs.anaconda.com/miniconda/install/#quick-command-line-install

Install docker https://docs.docker.com/engine/install/ubuntu/

or 

```
sudo apt install docker.io
```

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo usermod -aG docker $USER
```

install Xvfb
```
sudo apt-get install xvfb
```

### Install uv

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Python dependencies

From the repository root:

```
uv sync
```

This creates a local `.venv` and installs the dependencies from `pyproject.toml`.

### To create database engine

```
cd project
docker compose up
```

### Run the scraper

Run in the foreground:

```
uv run python project/src/main.py
```

Or use the restart script, which runs the scraper with `nohup` and writes `project/src/run.log`:

```
./project/run.sh
```
