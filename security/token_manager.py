"""Opaque token issuance (used by OTP/remember-me)."""
from __future__ import annotations

from utils.generators import generate_token


class TokenManager:
    @staticmethod
    def issue() -> str:
        return generate_token(32)
