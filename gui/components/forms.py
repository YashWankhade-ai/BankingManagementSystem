"""Form layout container."""
from __future__ import annotations

import customtkinter as ctk

from gui.theme import Theme


class FormGroup(ctk.CTkFrame):
    """Vertical form layout with consistent spacing."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

    def add(self, widget) -> None:
        widget.pack(in_=self, fill="x", pady=(0, 14))
