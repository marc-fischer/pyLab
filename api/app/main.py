from typing import Union
from fastapi import FastAPI, Query
from spd3303x import SPD3303X

app = FastAPI()
device = "192.168.178.168"


@app.get("/")
def read_root():
    return {"Hello": "World"}

# GETTER


@app.get("/voltage")
def read_voltage():
    with SPD3303X.ethernet_device(device) as dev:
        return {"VOLTAGE": [dev.CH1.get_voltage(), dev.CH2.get_voltage()], }


@app.get("/current")
def read_current():
    with SPD3303X.ethernet_device(device) as dev:
        return {"CURRENT": [dev.CH1.get_current(), dev.CH2.get_current()]}


@app.get("/status")
def read_status():
    with SPD3303X.ethernet_device(device) as dev:
        return {"SET": {"CURRENT": [dev.CH1.get_current(), dev.CH2.get_current()], "VOLTAGE": [dev.CH1.get_voltage(), dev.CH2.get_voltage()], "OUTPUT": []}, "IS": {"CURRENT": [dev.CH1.measure_current(), dev.CH2.measure_current()], "VOLTAGE": [dev.CH1.measure_voltage(), dev.CH2.measure_voltage()], "POWER": [dev.CH1.measure_power(), dev.CH2.measure_power()]}}


# SETTER
@app.post("/voltage")
def write_voltage(channel: int = Query(gt=0, le=2), voltage: float = Query(gt=0.000, le=32.000)):
    with SPD3303X.ethernet_device(device) as dev:
        if (channel == 1):
            dev.CH1.set_voltage(voltage)
        if (channel == 2):
            dev.CH2.set_voltage(voltage)
        return {"CHANNEL": channel, "VOLTAGE": voltage}


@app.post("/current")
def write_current(channel: int = Query(gt=0, le=2), current: float = Query(gt=0.000, le=3.200)):
    with SPD3303X.ethernet_device(device) as dev:
        if (channel == 1):
            dev.CH1.set_current(current)
        if (channel == 2):
            dev.CH2.set_current(current)
        return {"CHANNEL": channel, "CURRENT": current}


@app.post("/on")
def switch_on(channel: int = Query(gt=0, le=3)):
    with SPD3303X.ethernet_device(device) as dev:
        if (channel == 1):
            dev.CH1.set_output(True)
        if (channel == 2):
            dev.CH2.set_output(True)
        if (channel == 3):
            dev.CH3.set_output(True)
        return {"CHANNEL": channel, "OUTPUT": True}


@app.post("/off")
def switch_off(channel: int = Query(gt=0, le=3)):
    with SPD3303X.ethernet_device(device) as dev:
        if (channel == 1):
            dev.CH1.set_output(False)
        if (channel == 2):
            dev.CH2.set_output(False)
        if (channel == 3):
            dev.CH3.set_output(False)
        return {"CHANNEL": channel, "OUTPUT": False}
