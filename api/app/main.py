from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from plugins.spd3303x.spd3303x import SPD3303X
import time

class Settings: 
    device_ip = "192.168.178.168"
    channels = 2
    min_voltage = 0000
    max_voltage = 32000
    min_current = 0000
    max_current = 3200
    scaling = 1000
settings = Settings()

def create_app():
    app = FastAPI()
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:8080"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def read_root():
        return {"version": "1.0", "ps": {"device_ip": settings.device_ip, "channels": settings.channels, "min_voltage": settings.min_voltage, "max_voltage": settings.max_voltage, "min_current": settings.min_current, "max_current": settings.max_current, "scaling": settings.scaling}}

    # GETTER
    @app.get("/ps/voltage")
    def read_voltage():
        return {"VOLTAGE": [dev.CH1.get_voltage(), dev.CH2.get_voltage()], }


    @app.get("/ps/current")
    def read_current():
        return {"CURRENT": [dev.CH1.get_current(), dev.CH2.get_current()]}


    @app.get("/ps/status")
    def read_status():
        return {"SET": {"CURRENT": [dev.CH1.get_current(), dev.CH2.get_current()], "VOLTAGE": [dev.CH1.get_voltage(), dev.CH2.get_voltage()], "OUTPUT": []}, "IS": {"CURRENT": [dev.CH1.measure_current(), dev.CH2.measure_current()], "VOLTAGE": [dev.CH1.measure_voltage(), dev.CH2.measure_voltage()], "POWER": [dev.CH1.measure_power(), dev.CH2.measure_power()]}}


    @app.get("/ps/channel/{channel}")
    def read_channel(channel: int = Query(gt=1, le=settings.channels)):
        if(channel == 1):
            return {"SET": {"CURRENT": dev.CH1.get_current(), "VOLTAGE": dev.CH1.get_voltage()}, "IS": {"CURRENT": dev.CH1.measure_current(), "VOLTAGE": dev.CH1.measure_voltage(), "POWER": dev.CH1.measure_power()}}
        if(channel == 2):
             return {"SET": {"CURRENT": dev.CH2.get_current(), "VOLTAGE": dev.CH2.get_voltage()}, "IS": {"CURRENT": dev.CH2.measure_current(), "VOLTAGE": dev.CH2.measure_voltage(), "POWER": dev.CH2.measure_power()}}

    # SETTER
    @app.post("/ps/voltage")
    def write_voltage(channel: int = Query(gt=0, le=2), voltage: float = Query(gt=settings.min_voltage, le=settings.max_voltage)):
        request_time = time.ctime(time.time())
        if (channel == 1):
            dev.CH1.set_voltage(voltage / scaling)
            set_time = time.ctime(time.time())
        if (channel == 2):
            dev.CH2.set_voltage(voltage / scaling)
            set_time = time.ctime(time.time())
        return {"CHANNEL": channel, "VOLTAGE": voltage, "TIMING": {"REQ_TIME": request_time, "SET_TIME": set_time, "RET_TIME": time.ctime(time.time())}}


    @app.post("/ps/current")
    def write_current(channel: int = Query(gt=0, le=2), current: float = Query(gt=settings.min_current, le=settings.max_current)):
        request_time = time.ctime(time.time())
        if (channel == 1):
            dev.CH1.set_current(current / scaling)
            set_time = time.ctime(time.time())
        if (channel == 2):
            dev.CH2.set_current(current / scaling)
            set_time = time.ctime(time.time())
        return {"CHANNEL": channel, "CURRENT": current, "TIMING": {"REQ_TIME": request_time, "SET_TIME": set_time, "RET_TIME": time.ctime(time.time())}}


    @app.post("/ps/on")
    def switch_on(channel: int = Query(gt=0, le=3)):
        request_time = time.ctime(time.time())
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


    @app.post("/ps/off")
    def switch_off(channel: int = Query(gt=0, le=3)):
        request_time = time.ctime(time.time())
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

    return app

with SPD3303X.ethernet_device(settings.device_ip) as dev:
    app = create_app()