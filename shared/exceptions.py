"""
============================================================
Noor Custom Exceptions
============================================================
"""


class NoorError(Exception):
    pass


class CameraError(NoorError):
    pass


class StreamError(NoorError):
    pass


class ConfigError(NoorError):
    pass


class VisionError(NoorError):
    pass
