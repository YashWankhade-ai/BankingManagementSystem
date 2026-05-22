"""Admin repository."""
from __future__ import annotations

from typing import Optional

from database.db_connection import Database
from database.queries import AdminQ
from models.admin_model import Admin


class AdminRepository:
    def __init__(self, db: Optional[Database] = None) -> None:
        self._db = db or Database.instance()

    def by_username(self, username: str) -> Optional[Admin]:
        cur = self._db.connection.execute(AdminQ.BY_USERNAME, (username,))
        return Admin.maybe(cur.fetchone())

    def create(self, *, username: str, password_hash: str, role: str = "ADMIN") -> int:
        with self._db.transaction() as conn:
            cur = conn.execute(AdminQ.INSERT, (username, password_hash, role))
            return int(cur.lastrowid)
