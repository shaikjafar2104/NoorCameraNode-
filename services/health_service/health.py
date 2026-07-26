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


health_service = HealthService()
