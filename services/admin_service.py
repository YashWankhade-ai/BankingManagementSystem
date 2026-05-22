"""Admin operations service."""
from __future__ import annotations

from typing import List, Optional

from models.account_model import Account
from models.customer_model import Customer
from models.transaction_model import Transaction
from repositories.account_repository import AccountRepository
from repositories.admin_repository import AdminRepository
from repositories.customer_repository import CustomerRepository
from repositories.transaction_repository import TransactionRepository
from security.password_hasher import PasswordHasher


class AdminService:
    def __init__(
        self,
        admins: Optional[AdminRepository] = None,
        customers: Optional[CustomerRepository] = None,
        accounts: Optional[AccountRepository] = None,
        transactions: Optional[TransactionRepository] = None,
    ) -> None:
        self._admins = admins or AdminRepository()
        self._customers = customers or CustomerRepository()
        self._accounts = accounts or AccountRepository()
        self._transactions = transactions or TransactionRepository()

    def create_admin(self, username: str, password: str) -> int:
        return self._admins.create(
            username=username, password_hash=PasswordHasher.hash(password)
        )

    def search_customers(self, term: str) -> List[Customer]:
        term = (term or "").lower().strip()
        all_c = self._customers.all()
        if not term:
            return all_c
        return [
            c for c in all_c
            if term in c.full_name.lower()
            or term in c.username.lower()
            or term in c.mobile.lower()
        ]

    def all_accounts(self) -> List[Account]:
        return self._accounts.all()

    def all_transactions(self) -> List[Transaction]:
        return self._transactions.all()

    def freeze(self, account_id: int) -> None:
        self._accounts.update_status(account_id, "FROZEN")

    def unfreeze(self, account_id: int) -> None:
        self._accounts.update_status(account_id, "ACTIVE")

    def delete_customer(self, customer_id: int) -> None:
        self._customers.delete(customer_id)
