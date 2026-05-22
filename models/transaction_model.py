"""Transaction domain model."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class Transaction:
    id: int
    account_id: int
    type: str
    amount: float
    balance_after: float
    description: str
    created_at: str

    @staticmethod
    def from_row(row: Mapping[str, Any]) -> "Transaction":
        return Transaction(
            id=row["id"],
            account_id=row["account_id"],
            type=row["type"],
            amount=float(row["amount"]),
            balance_after=float(row["balance_after"]),
            description=row["description"] or "",
            created_at=row["created_at"],
        )
