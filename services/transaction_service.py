"""Deposit / withdraw / history."""
from __future__ import annotations

from typing import List, Optional

from database.db_connection import Database
from database.queries import AccountQ, TransactionQ
from models.transaction_model import Transaction
from repositories.account_repository import AccountRepository
from repositories.customer_repository import CustomerRepository
from repositories.transaction_repository import TransactionRepository
from security.pin_manager import PinManager
from services.validation_service import ValidationService
from utils.constants import (
    ACCOUNT_STATUS_ACTIVE,
    TX_DEPOSIT,
    TX_WITHDRAW,
)
from utils.exceptions import (
    AccountFrozenError,
    AuthenticationError,
    InsufficientFundsError,
    NotFoundError,
)
from utils.logger import get_logger

logger = get_logger(__name__)


class TransactionService:
    def __init__(
        self,
        accounts: Optional[AccountRepository] = None,
        customers: Optional[CustomerRepository] = None,
        transactions: Optional[TransactionRepository] = None,
        db: Optional[Database] = None,
    ) -> None:
        self._accounts = accounts or AccountRepository()
        self._customers = customers or CustomerRepository()
        self._transactions = transactions or TransactionRepository()
        self._db = db or Database.instance()

    # ---------------------------------------------------------------- deposit
    def deposit(self, account_id: int, amount: float, description: str = "Deposit") -> float:
        amount = ValidationService.validate_amount(amount)
        account = self._accounts.by_id(account_id)
        if not account:
            raise NotFoundError("Account not found.")
        if account.status != ACCOUNT_STATUS_ACTIVE:
            raise AccountFrozenError("Account is not active.")

        new_balance = round(account.balance + amount, 2)
        with self._db.transaction() as conn:
            conn.execute(AccountQ.UPDATE_BALANCE, (new_balance, account_id))
            conn.execute(
                TransactionQ.INSERT,
                (account_id, TX_DEPOSIT, amount, new_balance, description),
            )
        logger.info("Deposit %.2f to account %s", amount, account_id)
        return new_balance

    # --------------------------------------------------------------- withdraw
    def withdraw(
        self,
        *,
        account_id: int,
        amount: float,
        pin: str,
        description: str = "Withdraw",
    ) -> float:
        amount = ValidationService.validate_amount(amount)
        account = self._accounts.by_id(account_id)
        if not account:
            raise NotFoundError("Account not found.")
        if account.status != ACCOUNT_STATUS_ACTIVE:
            raise AccountFrozenError("Account is not active.")
        customer = self._customers.by_id(account.customer_id)
        if not customer:
            raise NotFoundError("Customer not found.")
        if not PinManager.verify(pin or "", customer.pin_hash):
            raise AuthenticationError("Invalid PIN.")
        if amount > account.balance:
            raise InsufficientFundsError("Insufficient balance.")

        new_balance = round(account.balance - amount, 2)
        with self._db.transaction() as conn:
            conn.execute(AccountQ.UPDATE_BALANCE, (new_balance, account_id))
            conn.execute(
                TransactionQ.INSERT,
                (account_id, TX_WITHDRAW, amount, new_balance, description),
            )
        logger.info("Withdraw %.2f from account %s", amount, account_id)
        return new_balance

    # ---------------------------------------------------------------- history
    def history(self, account_id: int, search: str = "") -> List[Transaction]:
        if search.strip():
            return self._transactions.search(account_id, search.strip())
        return self._transactions.by_account(account_id)

    def all_transactions(self) -> List[Transaction]:
        return self._transactions.all()

    def balance(self, account_id: int) -> float:
        acc = self._accounts.by_id(account_id)
        if not acc:
            raise NotFoundError("Account not found.")
        return acc.balance
