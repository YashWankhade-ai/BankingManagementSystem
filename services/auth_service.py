"""Authentication service for customers and admins."""
from __future__ import annotations

from typing import Optional

from models.admin_model import Admin
from models.customer_model import Customer
from repositories.admin_repository import AdminRepository
from repositories.customer_repository import CustomerRepository
from security.password_hasher import PasswordHasher
from security.session_manager import SessionManager
from utils.constants import ROLE_ADMIN, ROLE_CUSTOMER
from utils.exceptions import AuthenticationError
from utils.logger import get_logger

logger = get_logger(__name__)


class AuthService:
    def __init__(
        self,
        customers: Optional[CustomerRepository] = None,
        admins: Optional[AdminRepository] = None,
        sessions: Optional[SessionManager] = None,
    ) -> None:
        self._customers = customers or CustomerRepository()
        self._admins = admins or AdminRepository()
        self._sessions = sessions or SessionManager.instance()

    def login_customer(self, username: str, password: str) -> Customer:
        if not username or not password:
            raise AuthenticationError("Username and password are required.")
        customer = self._customers.by_username(username.strip())
        if not customer or not PasswordHasher.verify(password, customer.password_hash):
            logger.warning("Failed customer login: %s", username)
            raise AuthenticationError("Invalid username or password.")
        self._sessions.login(
            user_id=customer.id, role=ROLE_CUSTOMER, username=customer.username
        )
        logger.info("Customer logged in: %s", customer.username)
        return customer

    def login_admin(self, username: str, password: str) -> Admin:
        if not username or not password:
            raise AuthenticationError("Username and password are required.")
        admin = self._admins.by_username(username.strip())
        if not admin or not PasswordHasher.verify(password, admin.password_hash):
            logger.warning("Failed admin login: %s", username)
            raise AuthenticationError("Invalid admin credentials.")
        self._sessions.login(
            user_id=admin.id, role=ROLE_ADMIN, username=admin.username
        )
        logger.info("Admin logged in: %s", admin.username)
        return admin

    def logout(self) -> None:
        self._sessions.logout()
