"""Input validation utilities."""
from __future__ import annotations

import re
from datetime import datetime

from utils.constants import MAX_TX_AMOUNT, MIN_PASSWORD_LEN, PIN_LENGTH
from utils.exceptions import ValidationError


_USERNAME_RE = re.compile(r"^[A-Za-z0-9_.]{3,32}$")
_MOBILE_RE = re.compile(r"^\+?\d{7,15}$")


class ValidationService:
    """Pure functions for input validation."""

    @staticmethod
    def require_non_empty(value: str, field: str) -> str:
        if value is None or not str(value).strip():
            raise ValidationError(f"{field} is required.")
        return str(value).strip()

    @staticmethod
    def validate_full_name(name: str) -> str:
        name = ValidationService.require_non_empty(name, "Full name")
        if len(name) < 2 or len(name) > 80:
            raise ValidationError("Full name must be 2-80 characters.")
        return name

    @staticmethod
    def validate_dob(dob: str) -> str:
        dob = ValidationService.require_non_empty(dob, "Date of birth")
        try:
            d = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError as e:
            raise ValidationError("DOB must be in YYYY-MM-DD format.") from e
        if d > datetime.now():
            raise ValidationError("DOB cannot be in the future.")
        return dob

    @staticmethod
    def validate_mobile(mobile: str) -> str:
        mobile = ValidationService.require_non_empty(mobile, "Mobile")
        if not _MOBILE_RE.match(mobile):
            raise ValidationError("Mobile must be 7-15 digits, optional leading +.")
        return mobile

    @staticmethod
    def validate_address(address: str) -> str:
        address = ValidationService.require_non_empty(address, "Address")
        if len(address) > 250:
            raise ValidationError("Address too long (max 250).")
        return address

    @staticmethod
    def validate_username(username: str) -> str:
        username = ValidationService.require_non_empty(username, "Username")
        if not _USERNAME_RE.match(username):
            raise ValidationError(
                "Username must be 3-32 chars (letters, digits, _ or .)."
            )
        return username

    @staticmethod
    def validate_password(password: str) -> str:
        if not password or len(password) < MIN_PASSWORD_LEN:
            raise ValidationError(
                f"Password must be at least {MIN_PASSWORD_LEN} characters."
            )
        if not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
            raise ValidationError("Password must contain letters and digits.")
        return password

    @staticmethod
    def validate_pin(pin: str) -> str:
        if not pin or not pin.isdigit() or len(pin) != PIN_LENGTH:
            raise ValidationError(f"PIN must be exactly {PIN_LENGTH} digits.")
        return pin

    @staticmethod
    def validate_amount(amount_str: str | float) -> float:
        try:
            amount = float(amount_str)
        except (TypeError, ValueError) as e:
            raise ValidationError("Amount must be a number.") from e
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        if amount > MAX_TX_AMOUNT:
            raise ValidationError(f"Amount exceeds maximum of {MAX_TX_AMOUNT:,.2f}.")
        return round(amount, 2)
