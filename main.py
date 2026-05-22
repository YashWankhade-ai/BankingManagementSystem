"""Application entry point."""
from __future__ import annotations

import sys
import traceback

from config import CONFIG
from database.migrations import run_migrations
from utils.logger import get_logger

logger = get_logger("main")


def main() -> int:
    logger.info("Starting %s v%s", CONFIG.APP_NAME, CONFIG.APP_VERSION)
    try:
        run_migrations()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to initialize database: %s", exc)
        print("Database initialization failed. See logs/app.log.", file=sys.stderr)
        return 1

    try:
        from gui.app import BankingApp
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to import GUI: %s", exc)
        print(
            "GUI dependencies missing. Run: pip install -r requirements.txt",
            file=sys.stderr,
        )
        traceback.print_exc()
        return 2

    try:
        app = BankingApp()
        app.mainloop()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unhandled exception: %s", exc)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
