"""
============================================================
Project : Noor AI Home Platform
Module  : AI Detector
Version : 0.1.0
============================================================
"""

from shared.logger import logger
from ai.results import results


class AIDetector:

    def __init__(self):

        logger.info("AI Detector Initialized")

    def detect(self, frame):

        """
        Dummy detector.

        Real YOLO detector will be added later.
        """

        detections = [
            {
                "class": "person",
                "confidence": 1.00,
                "box": [100, 100, 250, 450]
            }
        ]

        results.update(detections)

        return detections


ai_detector = AIDetector()


if __name__ == "__main__":

    detector = AIDetector()

    data = detector.detect(None)

    print(data)
