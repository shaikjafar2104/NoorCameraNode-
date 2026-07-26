"""
============================================================
Project : Noor AI Home Platform
Module  : Camera Watchdog
Version : 1.0.0
============================================================
"""

import threading
import time

from shared.logger import logger
from shared.camera_state import camera_state


class CameraWatchdog:

    def __init__(self):

        self.running = False

        self.thread = None

        self.timeout = 5

        self.callback = None

    # -------------------------------------------------

    def set_callback(self, callback):

        self.callback = callback

    # -------------------------------------------------

    def loop(self):

        logger.info("Camera Watchdog Started")

        while self.running:

            now = time.time()

            if camera_state.connected:

                elapsed = now - camera_state.last_frame_time

                if elapsed > self.timeout:

                    logger.warning(

                        f"No frames received for {elapsed:.1f}s"

                    )

                    camera_state.reconnect()

                    if self.callback:

                        try:

                            self.callback()

                        except Exception as ex:

                            logger.error(

                                f"Watchdog callback failed: {ex}"

                            )

            time.sleep(1)

        logger.info("Camera Watchdog Stopped")

    # -------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )

        self.thread.start()

    # -------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread:

            self.thread.join(timeout=2)


watchdog = CameraWatchdog()
