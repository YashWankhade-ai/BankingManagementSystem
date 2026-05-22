"""Generic helpers."""
from __future__ import annotations

from datetime import datetime


def format_currency(amount: float, symbol: str = "₹") -> str:
    return f"{symbol}{amount:,.2f}"


def parse_iso(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")


def fmt_date(ts: str) -> str:
    try:
        return parse_iso(ts).strftime("%b %d, %Y · %H:%M")
    except Exception:
        return ts
