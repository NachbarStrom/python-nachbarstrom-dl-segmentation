#!/bin/bash
sudo apt-get upgrade -y
sudo apt-get update -y
sudo apt-get install libsm6 -y
sudo apt-get install libgtk2.0-dev -y

sudo bash scripts/install_python36.sh
python3.6 -m venv env-prod
source env-prod/bin/activate

sudo $(which python) -m pip install --upgrade setuptools
sudo $(which python) -m pip install -r requirements.txt
