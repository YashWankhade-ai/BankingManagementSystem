"""Reusable input widgets."""
from __future__ import annotations

from typing import Optional

import customtkinter as ctk

from gui.theme import Theme


class LabeledEntry(ctk.CTkFrame):
    """Label + entry composite."""

    def __init__(
        self,
        master,
        label: str,
        placeholder: str = "",
        show: Optional[str] = None,
        width: int = 320,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._label = ctk.CTkLabel(
            self,
            text=label.upper(),
            anchor="w",
            text_color=Theme.TEXT_MUTED,
            font=Theme.FONT_SMALL,
        )
        self._label.pack(fill="x", padx=2, pady=(0, 6))
        self._entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            show=show,
            width=width,
            height=42,
            corner_radius=Theme.RADIUS_SM,
            border_color=Theme.BORDER,
            fg_color=Theme.SURFACE_2,
            text_color=Theme.TEXT,
            font=Theme.FONT_BODY,
        )
        self._entry.pack(fill="x", padx=0)

    def get(self) -> str:
        return self._entry.get()

    def set(self, value: str) -> None:
        self._entry.delete(0, "end")
        self._entry.insert(0, value)

    def focus(self) -> None:  # type: ignore[override]
        self._entry.focus()

    @property
    def entry(self) -> ctk.CTkEntry:
        return self._entry


class LabeledTextarea(ctk.CTkFrame):
    def __init__(self, master, label: str, height: int = 80, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        ctk.CTkLabel(
            self,
            text=label.upper(),
            anchor="w",
            text_color=Theme.TEXT_MUTED,
            font=Theme.FONT_SMALL,
        ).pack(fill="x", padx=2, pady=(0, 6))
        self._text = ctk.CTkTextbox(
            self,
            height=height,
            corner_radius=Theme.RADIUS_SM,
            border_width=1,
            border_color=Theme.BORDER,
            fg_color=Theme.SURFACE_2,
            text_color=Theme.TEXT,
            font=Theme.FONT_BODY,
        )
        self._text.pack(fill="x")

    def get(self) -> str:
        return self._text.get("1.0", "end").strip()

    def set(self, value: str) -> None:
        self._text.delete("1.0", "end")
        self._text.insert("1.0", value)
