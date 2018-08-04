#!/bin/bash
sudo apt-get upgrade -y
sudo apt-get update -y
sudo apt-get install libsm6 -y
sudo apt-get install libgtk2.0-dev -y

sudo apt-get install python3-dev python3-venv python3-pip -y
python3 -m venv env-prod
source env-prod/bin/activate

sudo python3 -m pip install --upgrade setuptools
sudo python3 -m pip install -r requirements-prod.txt
