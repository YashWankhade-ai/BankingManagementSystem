"""Centralized logging setup."""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from config import CONFIG

_initialized = False


def _init() -> None:
    global _initialized
    if _initialized:
        return
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    formatter = logging.Formatter(fmt)

    file_h = RotatingFileHandler(
        CONFIG.LOG_FILE, maxBytes=2_000_000, backupCount=3, encoding="utf-8"
    )
    file_h.setFormatter(formatter)

    stream_h = logging.StreamHandler()
    stream_h.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(file_h)
    root.addHandler(stream_h)
    _initialized = True


def get_logger(name: str) -> logging.Logger:
    _init()
    return logging.getLogger(name)
