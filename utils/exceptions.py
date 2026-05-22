"""Domain-specific exceptions."""
from __future__ import annotations


class BankingError(Exception):
    """Base error for the banking domain."""


class ValidationError(BankingError):
    """Invalid input from the user."""


class AuthenticationError(BankingError):
    """Login or PIN failure."""


class NotFoundError(BankingError):
    """Resource not found."""


class InsufficientFundsError(BankingError):
    """Withdraw amount exceeds available balance."""


class AccountFrozenError(BankingError):
    """Operation rejected because the account is frozen/closed."""


class DuplicateError(BankingError):
    """Unique constraint violation."""


class OtpError(BankingError):
    """OTP generation or verification failure."""
