"""
============================================================
Project : Noor AI Home Platform
Module  : Diagnostics
Version : 1.0.0
============================================================
"""

from shared.camera_state import camera_state
from shared.performance import performance
from shared.system_monitor import system_monitor


class Diagnostics:

    def snapshot(self):

        return {

            "camera": camera_state.to_dict(),

            "performance": performance.snapshot(),

            "system": system_monitor.snapshot()

        }

    # -------------------------------------------------

    def health(self):

        camera = camera_state.to_dict()

        return {

            "status": (
                "healthy"
                if camera["connected"]
                else "degraded"
            ),

            "camera": camera["connected"],

            "fps": camera["fps"],

            "frames": camera["frames"],

            "drops": camera["dropped_frames"],

            "reconnects": camera["reconnects"]

        }


diagnostics = Diagnostics()
