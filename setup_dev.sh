#! /usr/bin/bash
sudo apt-get update
sudo apt-get install rpi.gpio

# Dev Setup
REQS_FILE=requirements-dev
.venv/bin/python3 -m pip install --upgrade pip pip-tools
.venv/bin/python3 -m piptools compile ${REQS_FILE}.in --output-file ${REQS_FILE}.txt --strip-extras && .venv/bin/python3 -m pip install -r ${REQS_FILE}.txt --no-deps

# Release Only
# python3 -m venv .venv
# .venv/bin/python3 -m pip install -U pip pip-tools
# .venv/bin/python3 -m piptools compile --generate-hashes requirements.in --output-file requirements.txt
# .venv/bin/python3 -m pip install -r requirements.txt --require-hashes --no-deps --only-binary :all:
