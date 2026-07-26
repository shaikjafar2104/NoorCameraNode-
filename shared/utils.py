"""
============================================================
Project : Noor AI
Module  : Shared Utilities
Version : 1.0.0
============================================================
"""

import os
import time
from datetime import datetime


# ---------------------------------------------------------
# Time
# ---------------------------------------------------------

def now():

    return datetime.now()


def timestamp():

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def current_time():

    return time.time()


def sleep(seconds):

    time.sleep(seconds)


# ---------------------------------------------------------
# File
# ---------------------------------------------------------

def file_exists(path):

    return os.path.exists(path)


def make_directory(path):

    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------
# Size
# ---------------------------------------------------------

def bytes_to_mb(size):

    return round(size / (1024 * 1024), 2)


# ---------------------------------------------------------
# Math
# ---------------------------------------------------------

def clamp(value, minimum, maximum):

    return max(minimum, min(value, maximum))


# ---------------------------------------------------------
# Boolean
# ---------------------------------------------------------

def yes_no(value):

    return "Yes" if value else "No"
