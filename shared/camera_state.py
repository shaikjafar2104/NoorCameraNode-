"""
============================================================
Project : Noor AI Home Platform
Module  : Camera State
Version : 1.0.0
============================================================
"""

from dataclasses import dataclass, field
from threading import Lock
from time import time


@dataclass
class CameraState:

    connected: bool = False

    width: int = 0
    height: int = 0

    fps: float = 0.0

    frames: int = 0

    dropped_frames: int = 0

    reconnect_count: int = 0

    last_frame_time: float = 0.0

    started_at: float = field(default_factory=time)

    lock: Lock = field(default_factory=Lock)

    # -----------------------------------------------------

    def set_connected(self, value: bool):

        with self.lock:
            self.connected = value

    # -----------------------------------------------------

    def update_resolution(
        self,
        width: int,
        height: int
    ):

        with self.lock:

            self.width = width
            self.height = height

    # -----------------------------------------------------

    def update_fps(self, fps: float):

        with self.lock:
            self.fps = round(fps, 2)

    # -----------------------------------------------------

    def add_frame(self):

        with self.lock:

            self.frames += 1
            self.last_frame_time = time()

    # -----------------------------------------------------

    def add_drop(self):

        with self.lock:
            self.dropped_frames += 1

    # -----------------------------------------------------

    def reconnect(self):

        with self.lock:
            self.reconnect_count += 1

    # -----------------------------------------------------

    def uptime(self):

        return round(time() - self.started_at, 1)

    # -----------------------------------------------------

    def to_dict(self):

        with self.lock:

            return {

                "connected": self.connected,

                "resolution": f"{self.width}x{self.height}",

                "fps": self.fps,

                "frames": self.frames,

                "dropped_frames": self.dropped_frames,

                "reconnects": self.reconnect_count,

                "uptime": self.uptime()

            }


camera_state = CameraState()
