#! /usr/bin/bash
sudo apt-get update
sudo apt-get install rpi.gpio

# Release Only
python3 -m venv .venv
.venv/bin/python3 -m pip install -U pip pip-tools
.venv/bin/python3 -m piptools compile --generate-hashes requirements.in --output-file requirements.txt
.venv/bin/python3 -m pip install -r requirements.txt --require-hashes --no-deps --only-binary :all:

# TODO: create stabdalone dist and edit crontab to run script on RPi boot
# https://www.circuitbasics.com/starting-programs-automatically-using-cron-on-a-raspberry-pi/