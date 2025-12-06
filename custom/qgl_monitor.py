#!/usr/bin/env python3
import re
import time
import requests

LOG = "/home/biqu/printer_data/logs/klippy.log"
API = "http://127.0.0.1:7125/printer/gcode/script"

# Regex ultra-robuste
range_pattern = re.compile(r"Probed\s*points\s*range:\s*([0-9]*\.[0-9]+)")

last_qgl = False
captured = False

def send(val):
    cmd = f"SET_GCODE_VARIABLE MACRO=QGL_RANGE VARIABLE=value VALUE={val}"
    requests.post(API, json={"script": cmd})

def follow(path):
    f = open(path, "r")
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.05)
            continue
        yield line

for line in follow(LOG):
    # Détecte début de QGL
    if "QUAD_GANTRY_LEVEL" in line and "probe" not in line:
        last_qgl = True
        captured = False

    if last_qgl and not captured:
        m = range_pattern.search(line)
        if m:
            send(m.group(1))
            captured = True

    # Détecte fin QGL
    if last_qgl and "Gantry-relative probe points" in line:
        last_qgl = False
