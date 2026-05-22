"""Auth tests."""
from __future__ import annotations

import unittest

from tests import setup_temp_db


class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        setup_temp_db()
        from services.account_service import AccountService
        from services.auth_service import AuthService

        cls.accounts = AccountService()
        cls.auth = AuthService()

        cls.accounts.register_customer(
            full_name="Alice Tester",
            dob="1990-01-01",
            mobile="+91551234567",
            address="1 Test Street",
            username="atul",
            password="Strong123",
            pin="1234",
            initial_deposit=100,
        )

    def test_login_success(self) -> None:
        c = self.auth.login_customer("atul", "Strong123")
        self.assertEqual(c.username, "atul")

    def test_login_failure(self) -> None:
        from utils.exceptions import AuthenticationError
        with self.assertRaises(AuthenticationError):
            self.auth.login_customer("atul", "wrong")

    def test_admin_seed_login(self) -> None:
        from config import CONFIG
        admin = self.auth.login_admin(CONFIG.DEFAULT_ADMIN_USERNAME, CONFIG.DEFAULT_ADMIN_PASSWORD)
        self.assertEqual(admin.role, "ADMIN")


if __name__ == "__main__":
    unittest.main()
