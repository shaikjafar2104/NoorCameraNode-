"""
============================================================
Project : Noor AI Home Platform
Module  : Configuration Manager
Version : 1.0.0
============================================================
"""

from pathlib import Path
import threading
import yaml

from shared.logger import logger


CONFIG_FILE = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "camera.yaml"
)


class ConfigManager:

    def __init__(self):
        self._config = {}
        self._lock = threading.Lock()
        self.load()

    # -----------------------------------------------------
    def load(self):
        with self._lock:
            if not CONFIG_FILE.exists():
                raise FileNotFoundError(
                    f"Config file not found: {CONFIG_FILE}"
                )

            with open(
                CONFIG_FILE,
                "r",
                encoding="utf-8"
            ) as f:
                self._config = yaml.safe_load(f) or {}

            logger.info("Configuration Loaded")
            return self._config

    # -----------------------------------------------------
    def reload(self):
        logger.info("Reloading Configuration")
        return self.load()

    # -----------------------------------------------------
    def get(self, key, default=None):
        with self._lock:
            keys = key.split(".")
            value = self._config

            for k in keys:
                if not isinstance(value, dict):
                    return default
                value = value.get(k)
                if value is None:
                    return default

            return value

    # -----------------------------------------------------
    def set(self, key, value):
        with self._lock:
            keys = key.split(".")
            data = self._config

            for k in keys[:-1]:
                data = data.setdefault(k, {})

            data[keys[-1]] = value

    # -----------------------------------------------------
    def save(self):
        with self._lock:
            with open(
                CONFIG_FILE,
                "w",
                encoding="utf-8"
            ) as f:
                yaml.safe_dump(
                    self._config,
                    f,
                    sort_keys=False
                )

            logger.info("Configuration Saved")

    # -----------------------------------------------------
    def as_dict(self):
        with self._lock:
            return dict(self._config)


_manager = ConfigManager()


def load_config():
    return _manager.as_dict()


def reload_config():
    return _manager.reload()


def get_config(key, default=None):
    return _manager.get(key, default)
