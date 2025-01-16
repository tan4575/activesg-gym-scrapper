# activesg-gym-scrapper

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

### To create the conda env

```
conda env create -f environment.yml
```

### To create database engine

```
docker compose up
```

