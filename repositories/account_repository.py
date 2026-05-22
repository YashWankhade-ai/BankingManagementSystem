"""Account repository."""
from __future__ import annotations

from typing import List, Optional

from database.db_connection import Database
from database.queries import AccountQ
from models.account_model import Account


class AccountRepository:
    def __init__(self, db: Optional[Database] = None) -> None:
        self._db = db or Database.instance()

    def create(self, *, account_number: str, customer_id: int, balance: float) -> int:
        with self._db.transaction() as conn:
            cur = conn.execute(AccountQ.INSERT, (account_number, customer_id, balance))
            return int(cur.lastrowid)

    def by_id(self, account_id: int) -> Optional[Account]:
        cur = self._db.connection.execute(AccountQ.BY_ID, (account_id,))
        return Account.maybe(cur.fetchone())

    def by_number(self, account_number: str) -> Optional[Account]:
        cur = self._db.connection.execute(AccountQ.BY_NUMBER, (account_number,))
        return Account.maybe(cur.fetchone())

    def by_customer(self, customer_id: int) -> List[Account]:
        cur = self._db.connection.execute(AccountQ.BY_CUSTOMER, (customer_id,))
        return [Account.from_row(r) for r in cur.fetchall()]

    def all(self) -> List[Account]:
        cur = self._db.connection.execute(AccountQ.ALL)
        return [Account.from_row(r) for r in cur.fetchall()]

    def update_balance(self, account_id: int, balance: float) -> None:
        with self._db.transaction() as conn:
            conn.execute(AccountQ.UPDATE_BALANCE, (balance, account_id))

    def update_status(self, account_id: int, status: str) -> None:
        with self._db.transaction() as conn:
            conn.execute(AccountQ.UPDATE_STATUS, (status, account_id))

    def delete(self, account_id: int) -> None:
        with self._db.transaction() as conn:
            conn.execute(AccountQ.DELETE, (account_id,))
