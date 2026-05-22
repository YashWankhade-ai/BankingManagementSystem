"""PIN hashing — reuses bcrypt with a smaller cost for fast verification."""
from __future__ import annotations

import bcrypt


class PinManager:
    """Hash & verify numeric account PINs."""

    ROUNDS = 10

    @staticmethod
    def hash(pin: str) -> str:
        salt = bcrypt.gensalt(rounds=PinManager.ROUNDS)
        return bcrypt.hashpw(pin.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify(pin: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(pin.encode("utf-8"), hashed.encode("utf-8"))
        except Exception:
            return False
