"""Database migrations / bootstrap."""
from __future__ import annotations

from pathlib import Path

from config import CONFIG
from database.db_connection import Database
from security.password_hasher import PasswordHasher
from utils.logger import get_logger

logger = get_logger(__name__)


def run_migrations() -> None:
    """Create tables and seed default admin if missing."""
    import shutil
    db_file = Path(CONFIG.DB_PATH)
    if not db_file.exists():
        src = Path(CONFIG.SCHEMA_PATH).parent / "banking.db"
        if src.exists() and src.resolve() != db_file.resolve():
            shutil.copy2(src, db_file)

    schema = Path(CONFIG.SCHEMA_PATH).read_text(encoding="utf-8")
    db = Database.instance()
    # executescript manages its own transactions; do not wrap.
    db.connection.executescript(schema)

    _seed_default_admin()
    logger.info("Database migrations completed.")


def _seed_default_admin() -> None:
    db = Database.instance()
    cur = db.connection.execute(
        "SELECT 1 FROM admins WHERE username = ?", (CONFIG.DEFAULT_ADMIN_USERNAME,)
    )
    if cur.fetchone():
        return
    pw_hash = PasswordHasher.hash(CONFIG.DEFAULT_ADMIN_PASSWORD)
    with db.transaction() as conn:
        conn.execute(
            "INSERT INTO admins(username, password_hash, role) VALUES(?,?,?)",
            (CONFIG.DEFAULT_ADMIN_USERNAME, pw_hash, "ADMIN"),
        )
    logger.info("Seeded default admin user '%s'.", CONFIG.DEFAULT_ADMIN_USERNAME)
