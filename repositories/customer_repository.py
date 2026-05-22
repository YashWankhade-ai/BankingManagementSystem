"""Customer repository — pure DB access."""
from __future__ import annotations

from typing import List, Optional

from database.db_connection import Database
from database.queries import CustomerQ
from models.customer_model import Customer


class CustomerRepository:
    def __init__(self, db: Optional[Database] = None) -> None:
        self._db = db or Database.instance()

    def create(
        self,
        *,
        full_name: str,
        dob: str,
        mobile: str,
        address: str,
        username: str,
        password_hash: str,
        pin_hash: str,
    ) -> int:
        with self._db.transaction() as conn:
            cur = conn.execute(
                CustomerQ.INSERT,
                (full_name, dob, mobile, address, username, password_hash, pin_hash),
            )
            return int(cur.lastrowid)

    def by_id(self, customer_id: int) -> Optional[Customer]:
        cur = self._db.connection.execute(CustomerQ.BY_ID, (customer_id,))
        return Customer.maybe(cur.fetchone())

    def by_username(self, username: str) -> Optional[Customer]:
        cur = self._db.connection.execute(CustomerQ.BY_USERNAME, (username,))
        return Customer.maybe(cur.fetchone())

    def all(self) -> List[Customer]:
        cur = self._db.connection.execute(CustomerQ.ALL)
        return [Customer.from_row(r) for r in cur.fetchall()]

    def delete(self, customer_id: int) -> None:
        with self._db.transaction() as conn:
            conn.execute(CustomerQ.DELETE, (customer_id,))

    def update_pin(self, customer_id: int, pin_hash: str) -> None:
        with self._db.transaction() as conn:
            conn.execute(CustomerQ.UPDATE_PIN, (pin_hash, customer_id))

    def update_password(self, customer_id: int, password_hash: str) -> None:
        with self._db.transaction() as conn:
            conn.execute(CustomerQ.UPDATE_PASSWORD, (password_hash, customer_id))
