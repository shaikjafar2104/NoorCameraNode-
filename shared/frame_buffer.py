"""
============================================================
Project : Noor AI Home Platform
Module  : Frame Buffer
Version : 1.0.0
============================================================
"""

import threading
import time

import cv2


class FrameBuffer:
    """
    Thread-safe latest frame storage.

    Stores only the newest frame in memory.
    """

    def __init__(self):

        self._frame = None

        self._timestamp = 0.0

        self._lock = threading.Lock()

    # -----------------------------------------------------

    def update(self, frame):

        if frame is None:
            return

        with self._lock:

            # Copy frame to prevent accidental modification
            self._frame = frame.copy()

            self._timestamp = time.time()

    # -----------------------------------------------------

    def get(self):

        with self._lock:

            if self._frame is None:
                return None

            return self._frame.copy()

    # -----------------------------------------------------

    def clear(self):

        with self._lock:

            self._frame = None

            self._timestamp = 0.0

    # -----------------------------------------------------

    def has_frame(self):

        with self._lock:

            return self._frame is not None

    # -----------------------------------------------------

    def age(self):

        with self._lock:

            if self._timestamp == 0:

                return None

            return round(

                time.time() - self._timestamp,

                3

            )

    # -----------------------------------------------------

    def resolution(self):

        with self._lock:

            if self._frame is None:

                return None

            h, w = self._frame.shape[:2]

            return {

                "width": w,

                "height": h

            }

    # -----------------------------------------------------

    def jpeg(self, quality=80):

        with self._lock:

            if self._frame is None:

                return None

            ok, buffer = cv2.imencode(

                ".jpg",

                self._frame,

                [

                    int(cv2.IMWRITE_JPEG_QUALITY),

                    quality

                ]

            )

            if not ok:

                return None

            return buffer.tobytes()


frame_buffer = FrameBuffer()
