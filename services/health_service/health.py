"""
============================================================
Project : Noor AI Home Platform
Module  : Health Service
Version : 1.0.0
============================================================
"""

import time

from shared.camera_state import camera_state
from shared.system_monitor import system_monitor
from shared.performance import performance
from shared.diagnostics import diagnostics
from shared.stats_manager import stats_manager


class HealthService:

    def snapshot(self):
        return {
            "status": "online" if camera_state.connected else "offline",
            "camera": camera_state.to_dict(),
            "stats": stats_manager.snapshot(),
            "performance": performance.snapshot(),
            "system": system_monitor.snapshot(),
            "diagnostics": diagnostics.snapshot(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_status(self):
        """Lightweight health summary for the /health endpoint.

        Reads already-running camera_service/runtime state only.
        Does NOT open a second camera device.
        """
        camera = camera_state.to_dict()
        last_frame_age = round(
            time.time() - camera_state.last_frame_time, 1
        ) if camera_state.last_frame_time > 0 else None
        return {
            "status": "healthy" if camera["connected"] else "degraded",
            "camera_connected": camera["connected"],
            "running": camera["connected"],
            "fps": camera["fps"],
            "resolution": camera["resolution"],
            "last_frame_age": last_frame_age,
            "frames": camera["frames"],
            "dropped_frames": camera["dropped_frames"],
            "reconnects": camera["reconnects"],
            "uptime": camera["uptime"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }


health_service = HealthService()
