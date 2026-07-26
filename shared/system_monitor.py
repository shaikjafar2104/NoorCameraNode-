"""
============================================================
Project : Noor AI Home Platform
Module  : System Monitor
Version : 1.0.0
============================================================
"""

import os
import shutil
import time

import psutil


class SystemMonitor:

    def cpu(self):

        return round(
            psutil.cpu_percent(interval=0.2),
            1
        )

    # -------------------------------------------------

    def memory(self):

        mem = psutil.virtual_memory()

        return {

            "percent": mem.percent,

            "used_mb": round(
                mem.used / 1024 / 1024
            ),

            "available_mb": round(
                mem.available / 1024 / 1024
            )

        }

    # -------------------------------------------------

    def disk(self):

        disk = shutil.disk_usage("/")

        return {

            "used_gb": round(
                disk.used / 1024**3,
                2
            ),

            "free_gb": round(
                disk.free / 1024**3,
                2
            )

        }

    # -------------------------------------------------

    def uptime(self):

        return round(
            time.time() - psutil.boot_time(),
            1
        )

    # -------------------------------------------------

    def process(self):

        p = psutil.Process(os.getpid())

        return {

            "pid": p.pid,

            "threads": p.num_threads(),

            "memory_mb": round(

                p.memory_info().rss /

                1024 /

                1024,

                2

            )

        }

    # -------------------------------------------------

    def snapshot(self):

        return {

            "cpu": self.cpu(),

            "memory": self.memory(),

            "disk": self.disk(),

            "process": self.process(),

            "uptime": self.uptime()

        }


system_monitor = SystemMonitor()
