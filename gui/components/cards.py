"""Card surfaces."""
from __future__ import annotations

import customtkinter as ctk

from gui.theme import Theme


class Card(ctk.CTkFrame):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(
            master,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER,
            **kwargs,
        )


class StatCard(ctk.CTkFrame):
    """Big numeric KPI card."""

    def __init__(self, master, title: str, value: str, accent: str = Theme.PRIMARY) -> None:
        super().__init__(
            master,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER,
        )
        self._accent_bar = ctk.CTkFrame(self, height=4, fg_color=accent, corner_radius=2)
        self._accent_bar.pack(fill="x", padx=18, pady=(18, 0))
        self._title = ctk.CTkLabel(
            self,
            text=title.upper(),
            text_color=Theme.TEXT_MUTED,
            font=Theme.FONT_SMALL,
            anchor="w",
        )
        self._title.pack(fill="x", padx=18, pady=(12, 0))
        self._value = ctk.CTkLabel(
            self,
            text=value,
            text_color=Theme.TEXT,
            font=Theme.FONT_NUMBER,
            anchor="w",
        )
        self._value.pack(fill="x", padx=18, pady=(4, 18))

    def set_value(self, value: str) -> None:
        self._value.configure(text=value)


class HeaderCard(ctk.CTkFrame):
    def __init__(self, master, title: str, subtitle: str = "") -> None:
        super().__init__(
            master,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER,
        )
        ctk.CTkLabel(
            self, text=title, font=Theme.FONT_H1, text_color=Theme.TEXT, anchor="w"
        ).pack(fill="x", padx=22, pady=(18, 4))
        if subtitle:
            ctk.CTkLabel(
                self,
                text=subtitle,
                font=Theme.FONT_BODY,
                text_color=Theme.TEXT_MUTED,
                anchor="w",
            ).pack(fill="x", padx=22, pady=(0, 18))
