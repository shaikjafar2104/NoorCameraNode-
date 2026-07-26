"""
============================================================
Project : Noor AI Home Platform
Module  : Statistics Manager
Version : 1.0.0
============================================================
"""

from threading import Lock
from shared.camera_state import camera_state


class StatsManager:

    def __init__(self):

        self.lock = Lock()

    # -------------------------------------------------

    def set_camera(self, connected: bool):

        camera_state.set_connected(connected)

    # -------------------------------------------------

    def update_resolution(

        self,

        width: int,

        height: int

    ):

        camera_state.update_resolution(

            width,

            height

        )

    # -------------------------------------------------

    def update_fps(

        self,

        fps: float

    ):

        camera_state.update_fps(fps)

    # -------------------------------------------------

    def add_frame(self):

        camera_state.add_frame()

    # -------------------------------------------------

    def add_drop(self):

        camera_state.add_drop()

    # -------------------------------------------------

    def reconnect(self):

        camera_state.reconnect()

    # -------------------------------------------------

    def snapshot(self):

        return camera_state.to_dict()


stats_manager = StatsManager()
