"""Transaction repository."""
from __future__ import annotations

from typing import List, Optional

from database.db_connection import Database
from database.queries import TransactionQ
from models.transaction_model import Transaction


class TransactionRepository:
    def __init__(self, db: Optional[Database] = None) -> None:
        self._db = db or Database.instance()

    def create(
        self,
        *,
        account_id: int,
        type_: str,
        amount: float,
        balance_after: float,
        description: str = "",
        conn=None,
    ) -> int:
        if conn is not None:
            cur = conn.execute(
                TransactionQ.INSERT,
                (account_id, type_, amount, balance_after, description),
            )
            return int(cur.lastrowid)
        with self._db.transaction() as c:
            cur = c.execute(
                TransactionQ.INSERT,
                (account_id, type_, amount, balance_after, description),
            )
            return int(cur.lastrowid)

    def by_account(self, account_id: int) -> List[Transaction]:
        cur = self._db.connection.execute(TransactionQ.BY_ACCOUNT, (account_id,))
        return [Transaction.from_row(r) for r in cur.fetchall()]

    def search(self, account_id: int, term: str) -> List[Transaction]:
        like = f"%{term}%"
        cur = self._db.connection.execute(TransactionQ.SEARCH, (account_id, like, like))
        return [Transaction.from_row(r) for r in cur.fetchall()]

    def all(self) -> List[Transaction]:
        cur = self._db.connection.execute(TransactionQ.ALL)
        return [Transaction.from_row(r) for r in cur.fetchall()]
