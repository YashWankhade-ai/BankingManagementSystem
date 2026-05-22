"""Thread-safe SQLite connection provider."""
from __future__ import annotations

import sqlite3
import threading
from contextlib import contextmanager
from typing import Iterator

from config import CONFIG


class Database:
    """Singleton-style SQLite connection manager."""

    _lock = threading.Lock()
    _instance: "Database | None" = None

    def __init__(self) -> None:
        self._conn = sqlite3.connect(
            CONFIG.DB_PATH, check_same_thread=False, isolation_level=None
        )
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON;")
        self._conn.execute("PRAGMA journal_mode = WAL;")
        self._txn_lock = threading.RLock()

    @classmethod
    def instance(cls) -> "Database":
        with cls._lock:
            if cls._instance is None:
                cls._instance = Database()
            return cls._instance

    @property
    def connection(self) -> sqlite3.Connection:
        return self._conn

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """Atomic transaction context."""
        with self._txn_lock:
            try:
                self._conn.execute("BEGIN")
                yield self._conn
                self._conn.execute("COMMIT")
            except Exception:
                self._conn.execute("ROLLBACK")
                raise

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass
