"""
============================================================
Project : Noor AI
Module  : Paths Manager
============================================================
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CONFIG = ROOT / "config"

LOGS = ROOT / "logs"

SHARED = ROOT / "shared"

SERVICES = ROOT / "services"

MODELS = ROOT / "models"

TESTS = ROOT / "tests"
