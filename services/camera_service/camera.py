"""
============================================================
Project : Noor AI Home Platform
Module : Camera Service
Version : 1.0.0
============================================================
"""

import threading
import time
import cv2

from shared.logger import logger
from shared.config_manager import load_config
from shared.frame_buffer import frame_buffer
from shared.stats_manager import stats_manager
from shared.performance import performance
from shared.watchdog import watchdog


class CameraService:

    def __init__(self):
        config = load_config()
        self.camera_index = config["camera"]["index"]
        self.width = config["video"]["width"]
        self.height = config["video"]["height"]
        self.target_fps = config["video"]["fps"]
        self.cap = None
        self.running = False
        self.thread = None
        self.frame_counter = 0
        self.fps_timer = time.time()
        self.lock = threading.Lock()

    # -----------------------------------------------------
    def connect(self):
        logger.info("=" * 60)
        logger.info("Noor Camera Service v1.0")
        logger.info("=" * 60)

        # Release old camera if already opened
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None

        # Try opening camera several times
        for attempt in range(1, 6):
            logger.info(f"Opening Camera (Attempt {attempt}/5)")
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)

            if self.cap.isOpened():
                logger.info("Camera Opened")
                break

            logger.warning("Camera unavailable... retrying")
            time.sleep(2)

        if self.cap is None or not self.cap.isOpened():
            logger.error("Cannot Open Camera")
            stats_manager.set_camera(False)
            return False

        # Configure camera
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.target_fps)

        time.sleep(2)

        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)

        logger.info("Camera Connected")
        logger.info(f"Resolution : {actual_width} x {actual_height}")
        logger.info(f"Target FPS : {self.target_fps}")
        logger.info(f"Camera FPS : {actual_fps}")

        stats_manager.set_camera(True)
        stats_manager.update_resolution(actual_width, actual_height)
        watchdog.set_callback(self.connect)

        return True

    # -----------------------------------------------------
    def capture_loop(self):
        logger.info("Capture Thread Started")
        failure_count = 0

        while self.running:
            if self.cap is None:
                logger.warning("Camera Handle Missing")
                time.sleep(1)
                if not self.connect():
                    continue

            capture_timer = performance.timer()
            success, frame = self.cap.read()
            capture_ms = performance.elapsed_ms(capture_timer)
            performance.update_capture(capture_ms)

            # -----------------------------------------
            # Read Failed
            # -----------------------------------------
            if not success or frame is None:
                failure_count += 1
                stats_manager.add_drop()

                if failure_count >= 10:
                    logger.warning(f"Camera Read Failed ({failure_count})")
                    stats_manager.reconnect()

                    try:
                        self.cap.release()
                    except Exception:
                        pass

                    self.cap = None
                    time.sleep(2)
                    self.connect()
                    failure_count = 0
                else:
                    time.sleep(0.02)
                    continue

            # -----------------------------------------
            # Read Success
            # -----------------------------------------
            failure_count = 0
            frame_buffer.update(frame)
            stats_manager.add_frame()
            self.frame_counter += 1

            # -----------------------------------------
            # FPS Update
            # -----------------------------------------
            elapsed = time.time() - self.fps_timer
            if elapsed >= 5:
                fps = self.frame_counter / elapsed
                stats_manager.update_fps(fps)
                logger.info(f"Average FPS : {fps:.2f}")
                self.frame_counter = 0
                self.fps_timer = time.time()

            # -----------------------------------------
            # CPU Friendly
            # -----------------------------------------
            if self.target_fps > 0:
                time.sleep(1 / (self.target_fps * 5))

        logger.info("Capture Thread Stopped")

    # -----------------------------------------------------
    def start(self):
        if self.running:
            logger.warning("Camera Service Already Running")
            return True

        logger.info("Starting Camera Service")

        if not self.connect():
            logger.error("Failed To Start Camera Service")
            return False

        self.running = True
        self.thread = threading.Thread(
            target=self.capture_loop,
            name="CameraCapture",
            daemon=True
        )
        self.thread.start()

        watchdog.set_callback(self.connect)
        watchdog.start()

        logger.info("Camera Service Started")
        return True

    # -----------------------------------------------------
    def stop(self):
        logger.info("Stopping Camera Service")
        self.running = False
        watchdog.stop()

        if self.thread is not None:
            self.thread.join(timeout=5)
            self.thread = None

        if self.cap is not None:
            try:
                self.cap.release()
            except Exception as ex:
                logger.error(f"Release Error : {ex}")
            self.cap = None

        stats_manager.set_camera(False)
        logger.info("Camera Released")
        logger.info("Camera Service Stopped")

    # -----------------------------------------------------
    def get_frame(self):
        return frame_buffer.get()


# ==========================================================
# Global Camera Service
# ==========================================================

camera_service = CameraService()


# ==========================================================
# Standalone Test
# ==========================================================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Noor Camera Service Test")
    logger.info("=" * 60)
