"""Test bootstrap — uses a temp DB."""
from __future__ import annotations

import os
import sys
import tempfile

# Ensure project root on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def setup_temp_db() -> None:
    """Point CONFIG.DB_PATH at a temp DB before importing repos."""
    import config as cfg

    tmp_dir = tempfile.mkdtemp(prefix="novabank_test_")
    db_path = os.path.join(tmp_dir, "test.db")
    object.__setattr__(cfg.CONFIG, "DB_PATH", db_path)

    # Reset DB singleton
    from database.db_connection import Database
    Database._instance = None  # type: ignore[attr-defined]

    from database.migrations import run_migrations
    run_migrations()
