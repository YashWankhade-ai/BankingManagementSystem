"""Account domain model."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class Account:
    id: int
    account_number: str
    customer_id: int
    balance: float
    status: str
    created_at: str
    updated_at: str

    @staticmethod
    def from_row(row: Mapping[str, Any]) -> "Account":
        return Account(
            id=row["id"],
            account_number=row["account_number"],
            customer_id=row["customer_id"],
            balance=float(row["balance"]),
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def maybe(row: Optional[Mapping[str, Any]]) -> Optional["Account"]:
        return Account.from_row(row) if row else None
