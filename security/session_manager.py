"""In-memory session manager."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from config import CONFIG
from utils.constants import ROLE_ADMIN, ROLE_CUSTOMER


@dataclass
class Session:
    user_id: int
    role: str
    username: str
    started_at: datetime = field(default_factory=datetime.utcnow)
    last_seen: datetime = field(default_factory=datetime.utcnow)

    def is_expired(self) -> bool:
        return datetime.utcnow() - self.last_seen > timedelta(
            minutes=CONFIG.SESSION_TIMEOUT_MIN
        )

    def touch(self) -> None:
        self.last_seen = datetime.utcnow()


class SessionManager:
    """Holds the active session for the desktop app (single-user)."""

    _lock = threading.Lock()
    _instance: "SessionManager | None" = None

    def __init__(self) -> None:
        self._session: Optional[Session] = None

    @classmethod
    def instance(cls) -> "SessionManager":
        with cls._lock:
            if cls._instance is None:
                cls._instance = SessionManager()
            return cls._instance

    def login(self, *, user_id: int, role: str, username: str) -> Session:
        assert role in (ROLE_ADMIN, ROLE_CUSTOMER)
        self._session = Session(user_id=user_id, role=role, username=username)
        return self._session

    def logout(self) -> None:
        self._session = None

    @property
    def current(self) -> Optional[Session]:
        if self._session and self._session.is_expired():
            self._session = None
        if self._session:
            self._session.touch()
        return self._session

    @property
    def is_authenticated(self) -> bool:
        return self.current is not None
