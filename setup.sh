#! /usr/bin/bash
sudo apt-get update
sudo apt-get install rpi.gpio
# Setup
.venv/bin/python3 -m pip install --upgrade pip pip-tools
.venv/bin/python3 -m piptools compile requirements.in --output-file requirements.txt --strip-extras && .venv/bin/python3 -m pip install -r requirements.txt --no-deps
