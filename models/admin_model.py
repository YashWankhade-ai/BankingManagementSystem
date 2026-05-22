"""Admin domain model."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class Admin:
    id: int
    username: str
    password_hash: str
    role: str
    created_at: str

    @staticmethod
    def from_row(row: Mapping[str, Any]) -> "Admin":
        return Admin(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            role=row["role"],
            created_at=row["created_at"],
        )

    @staticmethod
    def maybe(row: Optional[Mapping[str, Any]]) -> Optional["Admin"]:
        return Admin.from_row(row) if row else None
