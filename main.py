"""Application entry point."""
from __future__ import annotations

import os
import sys

from config import CONFIG
from database.migrations import run_migrations
from utils.logger import get_logger
from web.app import create_web_app

logger = get_logger("main")

# Top-level WSGI entry point for Vercel, Gunicorn, and Render Web Services
app = create_web_app()


def main() -> int:
    logger.info("Starting %s v%s", CONFIG.APP_NAME, CONFIG.APP_VERSION)
    try:
        run_migrations()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to initialize database: %s", exc)
        print("Database initialization failed. See logs/app.log.", file=sys.stderr)
        return 1

    # Check if running in cloud/server mode
    port_env = os.environ.get("PORT")
    cloud_mode = bool(port_env or os.environ.get("RENDER") or os.environ.get("VERCEL") or "--web" in sys.argv)

    if not cloud_mode:
        try:
            from gui.app import BankingApp
            gui_app = BankingApp()
            gui_app.mainloop()
            return 0
        except Exception as exc:  # noqa: BLE001
            logger.warning("Desktop GUI not available (%s). Falling back to Web Server.", exc)

    # Cloud or fallback mode: launch Flask Web Server
    web_port = int(port_env or 5000)
    print(f"Starting NovaBank Web Server on http://0.0.0.0:{web_port}")
    app.run(host="0.0.0.0", port=web_port, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
