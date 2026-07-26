"""
============================================================
Project : Noor AI
Module  : Global Constants
Version : 1.0.0
============================================================
"""


class Constants:

    # --------------------------------------------------
    # Project
    # --------------------------------------------------

    PROJECT_NAME = "Noor AI"

    CAMERA_NODE = "NoorCameraNode"

    BRAIN_NODE = "NoorBrain"

    VERSION = "1.0.0"

    # --------------------------------------------------
    # HTTP
    # --------------------------------------------------

    DEFAULT_TIMEOUT = 5

    STREAM_TIMEOUT = 10

    # --------------------------------------------------
    # Video
    # --------------------------------------------------

    DEFAULT_WIDTH = 1280

    DEFAULT_HEIGHT = 720

    DEFAULT_FPS = 15

    JPEG_QUALITY = 80

    # --------------------------------------------------
    # Vision
    # --------------------------------------------------

    PERSON_CONFIDENCE = 0.30

    MAX_QUEUE_SIZE = 5

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    FPS_UPDATE_INTERVAL = 5

    HEALTH_UPDATE_INTERVAL = 2

    # --------------------------------------------------
    # Threads
    # --------------------------------------------------

    THREAD_JOIN_TIMEOUT = 2

    # --------------------------------------------------
    # API
    # --------------------------------------------------

    HEALTH_ENDPOINT = "/health"

    STATS_ENDPOINT = "/stats"

    VIDEO_ENDPOINT = "/video_feed"

    DETECTIONS_ENDPOINT = "/detections"

    ZONES_ENDPOINT = "/zones"

    FRAME_SIZE_ENDPOINT = "/frame_size"


constants = Constants()
