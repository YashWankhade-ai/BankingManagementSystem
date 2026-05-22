"""bcrypt password/secret hashing."""
from __future__ import annotations

import bcrypt

from config import CONFIG


class PasswordHasher:
    """Encapsulates bcrypt hashing & verification."""

    @staticmethod
    def hash(plain: str) -> str:
        salt = bcrypt.gensalt(rounds=CONFIG.BCRYPT_ROUNDS)
        return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify(plain: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
        except Exception:
            return False
