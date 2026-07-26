"""
============================================================
Project : Noor AI Home Platform
Module  : Logger
Version : 1.0.0
============================================================
"""

import logging
import os
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "camera_node.log")

os.makedirs(LOG_DIR, exist_ok=True)


def build_logger():

    logger = logging.getLogger("NoorCameraNode")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(message)s"

    )

    # ------------------------------------------
    # Console
    # ------------------------------------------

    console = logging.StreamHandler()

    console.setFormatter(formatter)

    logger.addHandler(console)

    # ------------------------------------------
    # Rotating File
    # ------------------------------------------

    file_handler = RotatingFileHandler(

        LOG_FILE,

        maxBytes=10 * 1024 * 1024,

        backupCount=5,

        encoding="utf-8"

    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.propagate = False

    logger.info("=" * 60)

    logger.info("Logger Initialized")

    logger.info("=" * 60)

    return logger


logger = build_logger()


# ---------------------------------------------------------
# Standalone Test
# ---------------------------------------------------------

if __name__ == "__main__":

    logger.info("Info Test")

    logger.warning("Warning Test")

    logger.error("Error Test")

    logger.exception("Exception Test")
