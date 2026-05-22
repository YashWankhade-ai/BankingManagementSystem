"""Scrollable data table built on CTkScrollableFrame."""
from __future__ import annotations

from typing import Iterable, List, Sequence

import customtkinter as ctk

from gui.theme import Theme


class DataTable(ctk.CTkFrame):
    """Lightweight, themed table component."""

    def __init__(self, master, columns: Sequence[str], col_widths: Sequence[int] | None = None) -> None:
        super().__init__(
            master,
            fg_color=Theme.SURFACE,
            corner_radius=Theme.RADIUS_LG,
            border_width=1,
            border_color=Theme.BORDER,
        )
        self._columns = list(columns)
        self._widths = list(col_widths) if col_widths else [140] * len(columns)

        header = ctk.CTkFrame(self, fg_color=Theme.SURFACE_3, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        for col, w in zip(self._columns, self._widths):
            ctk.CTkLabel(
                header,
                text=col.upper(),
                width=w,
                anchor="w",
                text_color=Theme.TEXT_MUTED,
                font=Theme.FONT_SMALL,
            ).pack(side="left", padx=14, pady=12)

        self._body = ctk.CTkScrollableFrame(self, fg_color=Theme.SURFACE, corner_radius=0)
        self._body.pack(fill="both", expand=True)

    def set_rows(self, rows: Iterable[Sequence[str]]) -> None:
        for child in self._body.winfo_children():
            child.destroy()
        for i, row in enumerate(rows):
            bg = Theme.SURFACE if i % 2 == 0 else Theme.SURFACE_2
            r = ctk.CTkFrame(self._body, fg_color=bg, corner_radius=0)
            r.pack(fill="x")
            for value, w in zip(row, self._widths):
                ctk.CTkLabel(
                    r,
                    text=str(value),
                    width=w,
                    anchor="w",
                    text_color=Theme.TEXT,
                    font=Theme.FONT_BODY,
                ).pack(side="left", padx=14, pady=10)

    def empty_state(self, message: str = "No records") -> None:
        for child in self._body.winfo_children():
            child.destroy()
        ctk.CTkLabel(
            self._body,
            text=message,
            text_color=Theme.TEXT_DIM,
            font=Theme.FONT_BODY,
        ).pack(pady=30)
