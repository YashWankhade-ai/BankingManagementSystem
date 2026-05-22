"""OTP service — modular, mockable transport."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from config import CONFIG
from database.db_connection import Database
from database.queries import OtpQ
from security.password_hasher import PasswordHasher
from utils.exceptions import OtpError
from utils.generators import generate_otp
from utils.logger import get_logger

logger = get_logger(__name__)


class _MockSender:
    """Pretends to send an OTP — prints to console / log."""

    def send(self, subject: str, code: str) -> None:
        logger.info("[OTP MOCK] subject=%s code=%s", subject, code)
        print(f"[OTP MOCK] {subject} -> {code}")


class OtpService:
    def __init__(self, sender: Optional[_MockSender] = None) -> None:
        self._db = Database.instance()
        self._sender = sender or _MockSender()

    @property
    def enabled(self) -> bool:
        return CONFIG.OTP_ENABLED

    def issue(self, subject: str) -> str:
        if not subject:
            raise OtpError("Subject required.")
        code = generate_otp(CONFIG.OTP_LENGTH)
        code_hash = PasswordHasher.hash(code)
        expires = (
            datetime.utcnow() + timedelta(seconds=CONFIG.OTP_TTL_SECONDS)
        ).isoformat()
        with self._db.transaction() as conn:
            conn.execute(OtpQ.INSERT, (subject, code_hash, expires))
        self._sender.send(subject, code)
        return code  # returned for in-memory dev usage; do not log in prod

    def verify(self, subject: str, code: str) -> bool:
        cur = self._db.connection.execute(OtpQ.LATEST, (subject,))
        row = cur.fetchone()
        if not row:
            return False
        if datetime.fromisoformat(row["expires_at"]) < datetime.utcnow():
            return False
        if not PasswordHasher.verify(code, row["code_hash"]):
            return False
        with self._db.transaction() as conn:
            conn.execute(OtpQ.CONSUME, (row["id"],))
        return True
