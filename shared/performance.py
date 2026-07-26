"""
============================================================
Project : Noor AI Home Platform
Module  : Performance Monitor
Version : 1.0.0
============================================================
"""

from threading import Lock
from time import perf_counter


class PerformanceMonitor:

    def __init__(self):

        self.lock = Lock()

        self.capture_ms = 0.0
        self.encode_ms = 0.0
        self.network_ms = 0.0

        self.max_capture_ms = 0.0
        self.max_encode_ms = 0.0

        self.capture_samples = 0
        self.encode_samples = 0

    # -------------------------------------------------

    def update_capture(self, elapsed_ms: float):

        with self.lock:

            self.capture_samples += 1

            self.capture_ms = (
                (self.capture_ms * (self.capture_samples - 1))
                + elapsed_ms
            ) / self.capture_samples

            self.max_capture_ms = max(
                self.max_capture_ms,
                elapsed_ms
            )

    # -------------------------------------------------

    def update_encode(self, elapsed_ms: float):

        with self.lock:

            self.encode_samples += 1

            self.encode_ms = (
                (self.encode_ms * (self.encode_samples - 1))
                + elapsed_ms
            ) / self.encode_samples

            self.max_encode_ms = max(
                self.max_encode_ms,
                elapsed_ms
            )

    # -------------------------------------------------

    def update_network(self, elapsed_ms: float):

        with self.lock:
            self.network_ms = elapsed_ms

    # -------------------------------------------------

    def timer(self):

        return perf_counter()

    # -------------------------------------------------

    def elapsed_ms(self, start):

        return (perf_counter() - start) * 1000

    # -------------------------------------------------

    def snapshot(self):

        with self.lock:

            return {

                "capture_avg_ms": round(self.capture_ms, 2),

                "capture_max_ms": round(
                    self.max_capture_ms,
                    2
                ),

                "jpeg_avg_ms": round(
                    self.encode_ms,
                    2
                ),

                "jpeg_max_ms": round(
                    self.max_encode_ms,
                    2
                ),

                "network_ms": round(
                    self.network_ms,
                    2
                )

            }


performance = PerformanceMonitor()
