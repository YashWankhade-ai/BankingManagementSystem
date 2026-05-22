"""Domain models (immutable dataclasses)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class Customer:
    id: int
    full_name: str
    dob: str
    mobile: str
    address: str
    username: str
    password_hash: str
    pin_hash: str
    created_at: str
    updated_at: str

    @staticmethod
    def from_row(row: Mapping[str, Any]) -> "Customer":
        return Customer(
            id=row["id"],
            full_name=row["full_name"],
            dob=row["dob"],
            mobile=row["mobile"],
            address=row["address"],
            username=row["username"],
            password_hash=row["password_hash"],
            pin_hash=row["pin_hash"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def maybe(row: Optional[Mapping[str, Any]]) -> Optional["Customer"]:
        return Customer.from_row(row) if row else None
