"""Deposit / withdraw tests."""
from __future__ import annotations

import unittest

from tests import setup_temp_db


class TestTransactions(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        setup_temp_db()
        from services.account_service import AccountService
        from services.transaction_service import TransactionService

        cls.accounts = AccountService()
        cls.tx = TransactionService()
        c, a = cls.accounts.register_customer(
            full_name="Carla T", dob="1992-02-02", mobile="+15553334444",
            address="3 Test Ave", username="carla", password="Strong123",
            pin="9876", initial_deposit=500,
        )
        cls.customer_id = c.id
        cls.account_id = a.id

    def test_deposit(self) -> None:
        new_bal = self.tx.deposit(self.account_id, 100, "test deposit")
        self.assertEqual(new_bal, 600.00)

    def test_withdraw_with_pin(self) -> None:
        bal = self.tx.withdraw(account_id=self.account_id, amount=50, pin="9876")
        self.assertEqual(bal, 550.00)

    def test_withdraw_wrong_pin(self) -> None:
        from utils.exceptions import AuthenticationError
        with self.assertRaises(AuthenticationError):
            self.tx.withdraw(account_id=self.account_id, amount=10, pin="0000")

    def test_withdraw_insufficient_funds(self) -> None:
        from utils.exceptions import InsufficientFundsError
        with self.assertRaises(InsufficientFundsError):
            self.tx.withdraw(account_id=self.account_id, amount=10_000_00, pin="9876")

    def test_history_records_entries(self) -> None:
        history = self.tx.history(self.account_id)
        self.assertGreaterEqual(len(history), 1)


if __name__ == "__main__":
    unittest.main()
