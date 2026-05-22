"""Application configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class AppConfig:
    """Centralized, immutable application configuration."""

    APP_NAME: str = "NovaBank — Banking Management System"
    APP_VERSION: str = "1.0.0"

    # Database
    DB_PATH: str = str(BASE_DIR / "database" / "banking.db")
    SCHEMA_PATH: str = str(BASE_DIR / "database" / "schema.sql")

    # Logging
    LOG_DIR: str = str(BASE_DIR / "logs")
    LOG_FILE: str = str(BASE_DIR / "logs" / "app.log")

    # Security
    BCRYPT_ROUNDS: int = 12
    SESSION_TIMEOUT_MIN: int = 30

    # Features
    OTP_ENABLED: bool = False
    OTP_TTL_SECONDS: int = 300
    OTP_LENGTH: int = 6

    # Defaults
    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "Admin@123"

    # UI
    WINDOW_WIDTH: int = 1280
    WINDOW_HEIGHT: int = 800
    APPEARANCE_MODE: str = "dark"


CONFIG = AppConfig()

os.makedirs(CONFIG.LOG_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CONFIG.DB_PATH), exist_ok=True)
