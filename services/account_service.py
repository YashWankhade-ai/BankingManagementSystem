"""Customer / account creation business logic."""
from __future__ import annotations

import sqlite3
from typing import Optional

from models.account_model import Account
from models.customer_model import Customer
from repositories.account_repository import AccountRepository
from repositories.customer_repository import CustomerRepository
from security.password_hasher import PasswordHasher
from security.pin_manager import PinManager
from services.validation_service import ValidationService
from utils.exceptions import DuplicateError, NotFoundError
from utils.generators import generate_account_number
from utils.logger import get_logger

logger = get_logger(__name__)


class AccountService:
    def __init__(
        self,
        customers: Optional[CustomerRepository] = None,
        accounts: Optional[AccountRepository] = None,
    ) -> None:
        self._customers = customers or CustomerRepository()
        self._accounts = accounts or AccountRepository()

    # ---- creation ----------------------------------------------------------

    def register_customer(
        self,
        *,
        full_name: str,
        dob: str,
        mobile: str,
        address: str,
        username: str,
        password: str,
        pin: str,
        initial_deposit: float = 0.0,
    ) -> tuple[Customer, Account]:
        v = ValidationService
        full_name = v.validate_full_name(full_name)
        dob = v.validate_dob(dob)
        mobile = v.validate_mobile(mobile)
        address = v.validate_address(address)
        username = v.validate_username(username)
        v.validate_password(password)
        v.validate_pin(pin)
        deposit = float(initial_deposit or 0.0)
        if deposit < 0:
            from utils.exceptions import ValidationError
            raise ValidationError("Initial deposit cannot be negative.")

        if self._customers.by_username(username):
            raise DuplicateError("Username already exists.")

        try:
            customer_id = self._customers.create(
                full_name=full_name,
                dob=dob,
                mobile=mobile,
                address=address,
                username=username,
                password_hash=PasswordHasher.hash(password),
                pin_hash=PinManager.hash(pin),
            )
        except sqlite3.IntegrityError as e:
            raise DuplicateError("Username already exists.") from e

        # Account number — retry on rare collision
        for _ in range(5):
            number = generate_account_number()
            if not self._accounts.by_number(number):
                break
        account_id = self._accounts.create(
            account_number=number, customer_id=customer_id, balance=round(deposit, 2)
        )

        customer = self._customers.by_id(customer_id)
        account = self._accounts.by_id(account_id)
        assert customer and account
        logger.info("Registered customer %s with account %s", username, number)
        return customer, account

    # ---- queries -----------------------------------------------------------

    def get_customer_account(self, customer_id: int) -> Account:
        items = self._accounts.by_customer(customer_id)
        if not items:
            raise NotFoundError("No account found for this customer.")
        return items[0]

    def get_account_by_number(self, number: str) -> Account:
        acc = self._accounts.by_number(number)
        if not acc:
            raise NotFoundError(f"Account {number} not found.")
        return acc

    def list_all_customers(self) -> list[Customer]:
        return self._customers.all()

    def list_all_accounts(self) -> list[Account]:
        return self._accounts.all()

    def freeze(self, account_id: int) -> None:
        self._accounts.update_status(account_id, "FROZEN")
        logger.info("Account %s frozen.", account_id)

    def unfreeze(self, account_id: int) -> None:
        self._accounts.update_status(account_id, "ACTIVE")
        logger.info("Account %s unfrozen.", account_id)

    def delete_customer(self, customer_id: int) -> None:
        self._customers.delete(customer_id)
        logger.info("Customer %s deleted.", customer_id)
