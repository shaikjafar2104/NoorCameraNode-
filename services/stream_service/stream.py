"""
============================================================
Project : Noor AI Home Platform
Module  : Stream Service
Version : 1.0.0
============================================================
"""

import os
import time
import cv2

from fastapi import FastAPI
from fastapi.responses import (
    HTMLResponse,
    StreamingResponse
)

from services.camera_service.camera import camera_service
from services.health_service import health_service
from shared.camera_state import camera_state
from shared.stats_manager import stats_manager
from shared.performance import performance
from shared.system_monitor import system_monitor
from shared.diagnostics import diagnostics
from shared.config_manager import load_config
from shared.logger import logger

config = load_config()

app = FastAPI(
    title="Noor Camera Node",
    version="1.0.0"
)

START_TIME = time.time()
JPEG_QUALITY = 80


@app.on_event("startup")
def startup():
    logger.info("Starting Noor Camera Node")
    camera_service.start()


@app.on_event("shutdown")
def shutdown():
    logger.info("Stopping Noor Camera Node")
    camera_service.stop()

@app.get("/")
def home():
    return HTMLResponse(f"""
<html>
<head>
<title>Noor Camera Node</title>
<style>
body{{
    background:#202124;
    font-family:Arial;
    color:white;
    text-align:center;
}}
img{{
    width:900px;
    border:2px solid #00cc66;
    border-radius:10px;
}}
.card{{
    width:900px;
    margin:auto;
    background:#303134;
    padding:15px;
    border-radius:10px;
}}
a{{
    color:#00cc66;
    margin:12px;
    text-decoration:none;
}}
</style>
</head>
<body>
<h1>Noor Camera Node v1.0</h1>
<img src="/video_feed">
<br><br>
<div class="card">
<a href="/health">Health</a>
<a href="/stats">Stats</a>
<a href="/diagnostics">Diagnostics</a>
<a href="/system">System</a>
<a href="/config">Config</a>
<a href="/version">Version</a>
</div>
</body>
</html>
""")


# ==========================================================
# Health
# ==========================================================
@app.get("/health")
def health():
    return health_service.get_status()


# ==========================================================
# Stats
# ==========================================================
@app.get("/stats")
def stats():
    return stats_manager.snapshot()


# ==========================================================
# Diagnostics
# ==========================================================
@app.get("/diagnostics")
def diagnostics_api():
    return diagnostics.snapshot()


# ==========================================================
# System
# ==========================================================
@app.get("/system")
def system():
    return system_monitor.snapshot()


# ==========================================================
# Config
# ==========================================================
@app.get("/config")
def configuration():
    return config


# ==========================================================
# Version
# ==========================================================
@app.get("/version")
def version():
    return {
        "project": "Noor Camera Node",
        "version": "1.0.0"
    }


# ==========================================================
# Ping
# ==========================================================
@app.get("/ping")
def ping():
    return {
        "message": "pong"
    }


# ==========================================================
# Ready
# ==========================================================
@app.get("/ready")
def ready():
    return {
        "ready": camera_state.connected
    }


# ==========================================================
# Live
# ==========================================================
@app.get("/live")
def live():
    return {
        "live": True
    }


# ==========================================================
# MJPEG Generator
# ==========================================================
def generate():
    encode_param = [
        int(cv2.IMWRITE_JPEG_QUALITY),
        JPEG_QUALITY
    ]

    while True:
        frame = camera_service.get_frame()

        if frame is None:
            time.sleep(0.01)
            continue

        timer = performance.timer()
        ok, buffer = cv2.imencode(".jpg", frame, encode_param)
        performance.update_encode(performance.elapsed_ms(timer))

        if not ok:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + buffer.tobytes()
            + b'\r\n'
        )

        time.sleep(0.001)


# ==========================================================
# Video Feed
# ==========================================================
@app.get("/video_feed")
def video_feed():
    logger.info("Client Connected To Video Feed")
    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Expires": "0",
            "Connection": "close"
        }
    )


# ==========================================================
# Startup Log
# ==========================================================
logger.info("=" * 60)
logger.info("Noor Stream Service Loaded")
logger.info("=" * 60)
