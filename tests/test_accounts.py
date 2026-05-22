"""Account creation & validation tests."""
from __future__ import annotations

import unittest

from tests import setup_temp_db


class TestAccounts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        setup_temp_db()
        from services.account_service import AccountService
        cls.svc = AccountService()

    def test_register_and_fetch(self) -> None:
        c, a = self.svc.register_customer(
            full_name="shiv Tester",
            dob="1985-05-05",
            mobile="+15559876543",
            address="2 Test Lane",
            username="shiv",
            password="Strong123",
            pin="4321",
            initial_deposit=250.55,
        )
        self.assertEqual(a.balance, 250.55)
        self.assertEqual(a.status, "ACTIVE")
        self.assertEqual(len(a.account_number), 12)
        same = self.svc.get_customer_account(c.id)
        self.assertEqual(same.id, a.id)

    def test_duplicate_username_rejected(self) -> None:
        from utils.exceptions import DuplicateError

        self.svc.register_customer(
            full_name="C T", dob="1990-01-01", mobile="+91550000000",
            address="x", username="dup1", password="Strong123", pin="1111",
        )
        with self.assertRaises(DuplicateError):
            self.svc.register_customer(
                full_name="C T", dob="1990-01-01", mobile="+91550000000",
                address="x", username="dup1", password="Strong123", pin="1111",
            )

    def test_validation_password(self) -> None:
        from utils.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            self.svc.register_customer(
                full_name="x y", dob="1990-01-01", mobile="+91550000001",
                address="a", username="badpass", password="weak", pin="1111",
            )


if __name__ == "__main__":
    unittest.main()
