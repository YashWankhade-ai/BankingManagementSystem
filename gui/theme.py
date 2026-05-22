"""Design tokens for the application."""
from __future__ import annotations


class Theme:
    """Premium dark fintech palette."""

    # Surfaces
    BG = "#0B0F17"
    SURFACE = "#121826"
    SURFACE_2 = "#1A2233"
    SURFACE_3 = "#222C42"
    BORDER = "#243049"

    # Text
    TEXT = "#E6ECF5"
    TEXT_MUTED = "#8A95AD"
    TEXT_DIM = "#5B6478"

    # Brand
    PRIMARY = "#3D7BFF"
    PRIMARY_HOVER = "#5A91FF"
    PRIMARY_PRESSED = "#2C66E0"

    ACCENT = "#22D3A6"
    DANGER = "#F25C7A"
    WARNING = "#F2B544"
    SUCCESS = "#22C586"

    # Sidebar
    SIDEBAR_BG = "#0E1422"
    SIDEBAR_ACTIVE = "#1B2540"

    # Typography
    FONT_FAMILY = "Segoe UI"
    FONT_DISPLAY = ("Segoe UI", 28, "bold")
    FONT_H1 = ("Segoe UI", 22, "bold")
    FONT_H2 = ("Segoe UI", 18, "bold")
    FONT_H3 = ("Segoe UI", 14, "bold")
    FONT_BODY = ("Segoe UI", 13)
    FONT_BODY_BOLD = ("Segoe UI", 13, "bold")
    FONT_SMALL = ("Segoe UI", 11)
    FONT_LABEL = ("Segoe UI", 12, "bold")
    FONT_NUMBER = ("Segoe UI", 30, "bold")

    # Geometry
    RADIUS_SM = 8
    RADIUS = 12
    RADIUS_LG = 18
    PADDING = 16
