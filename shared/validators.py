"""
============================================================
Validators
============================================================
"""

import os


def validate_file(path):

    return os.path.isfile(path)


def validate_directory(path):

    return os.path.isdir(path)


def validate_positive(value):

    return value > 0


def validate_port(port):

    return 1 <= port <= 65535
