"""Random/identifier generators."""
from __future__ import annotations

import secrets
import time


def generate_account_number() -> str:
    """Generate a 12-digit unique account number."""
    ts = int(time.time()) % 1_000_000
    rnd = secrets.randbelow(1_000_000)
    return f"{ts:06d}{rnd:06d}"


def generate_token(nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)


def generate_otp(length: int = 6) -> str:
    upper = 10 ** length
    return f"{secrets.randbelow(upper):0{length}d}"
