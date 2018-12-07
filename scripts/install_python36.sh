#!/usr/bin/env bash
# setup Python3.6 with pip and venv
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.6-dev
sudo curl https://bootstrap.pypa.io/get-pip.py | sudo python3.6
sudo apt install python3.6-venv