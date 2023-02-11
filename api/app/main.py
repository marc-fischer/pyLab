from fastapi import FastAPI, Query
from spd3303x import SPD3303X
import time

app = FastAPI()
device_ip = "192.168.178.168"


@app.get("/")
def read_root():
    return {"version": "1.0", "device_ip": device_ip}

# GETTER
@app.get("/voltage")
def read_voltage():
    with SPD3303X.ethernet_device(device_ip) as dev:
        return {"VOLTAGE": [dev.CH1.get_voltage(), dev.CH2.get_voltage()], }


@app.get("/current")
def read_current():
    with SPD3303X.ethernet_device(device_ip) as dev:
        return {"CURRENT": [dev.CH1.get_current(), dev.CH2.get_current()]}


@app.get("/status")
def read_status():
    with SPD3303X.ethernet_device(device_ip) as dev:
        return {"SET": {"CURRENT": [dev.CH1.get_current(), dev.CH2.get_current()], "VOLTAGE": [dev.CH1.get_voltage(), dev.CH2.get_voltage()], "OUTPUT": []}, "IS": {"CURRENT": [dev.CH1.measure_current(), dev.CH2.measure_current()], "VOLTAGE": [dev.CH1.measure_voltage(), dev.CH2.measure_voltage()], "POWER": [dev.CH1.measure_power(), dev.CH2.measure_power()]}}


# SETTER
@app.post("/voltage")
def write_voltage(channel: int = Query(gt=0, le=2), voltage: float = Query(gt=0.000, le=32.000)):
    request_time = time.ctime(time.time())
    with SPD3303X.ethernet_device(device_ip) as dev:
        if (channel == 1):
            dev.CH1.set_voltage(voltage)
            set_time = time.ctime(time.time())
        if (channel == 2):
            dev.CH2.set_voltage(voltage)
            set_time = time.ctime(time.time())
        return {"CHANNEL": channel, "VOLTAGE": voltage, "TIMING": {"REQ_TIME": request_time, "SET_TIME": set_time, "RET_TIME": time.ctime(time.time())}}


@app.post("/current")
def write_current(channel: int = Query(gt=0, le=2), current: float = Query(gt=0.000, le=3.200)):
    request_time = time.ctime(time.time())
    with SPD3303X.ethernet_device(device_ip) as dev:
        if (channel == 1):
            dev.CH1.set_current(current)
            set_time = time.ctime(time.time())
        if (channel == 2):
            dev.CH2.set_current(current)
            set_time = time.ctime(time.time())
        return {"CHANNEL": channel, "CURRENT": current, "TIMING": {"REQ_TIME": request_time, "SET_TIME": set_time, "RET_TIME": time.ctime(time.time())}}


@app.post("/on")
def switch_on(channel: int = Query(gt=0, le=3)):
    request_time = time.ctime(time.time())
    with SPD3303X.ethernet_device(device_ip) as dev:
        if (channel == 1):
            dev.CH1.set_output(True)
            set_time = time.ctime(time.time())
        if (channel == 2):
            dev.CH2.set_output(True)
            set_time = time.ctime(time.time())
        if (channel == 3):
            dev.CH3.set_output(True)
            set_time = time.ctime(time.time())
        return {"CHANNEL": channel, "OUTPUT": True, "TIMING": {"REQ_TIME": request_time, "SET_TIME": set_time, "RET_TIME": time.ctime(time.time())}}


@app.post("/off")
def switch_off(channel: int = Query(gt=0, le=3)):
    request_time = time.ctime(time.time())
    with SPD3303X.ethernet_device(device_ip) as dev:
        if (channel == 1):
            dev.CH1.set_output(False)
            set_time = time.ctime(time.time())
        if (channel == 2):
            dev.CH2.set_output(False)
            set_time = time.ctime(time.time())
        if (channel == 3):
            dev.CH3.set_output(False)
            set_time = time.ctime(time.time())
        return {"CHANNEL": channel, "OUTPUT": False, "TIMING": {"REQ_TIME": request_time, "SET_TIME": set_time, "RET_TIME": time.ctime(time.time())}}
