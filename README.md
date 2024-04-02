# BLE Heart Pump Project

Getting heart rate signal from TICKRX bluetoth heart rate chest strap to drive a peristaltic pump to simulate a heart pumping blood.

# Gettting Started

```sh
python3 -m venv .venv
.venv/bin/python3 -m pip install --upgrade pip pip-tools
```

```sh
.venv/bin/python3 -m piptools compile requirements.in --output-file requirements.txt && .venv/bin/python3 -m pip install -r requirements.txt --no-deps
```

```sh
.venv/bin/python3 -m heartpump
```
