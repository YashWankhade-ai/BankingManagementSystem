"""Top bar component."""
from __future__ import annotations

import customtkinter as ctk

from gui.theme import Theme


class TopBar(ctk.CTkFrame):
    def __init__(self, master, title: str, user_label: str) -> None:
        super().__init__(master, height=64, fg_color=Theme.BG, corner_radius=0)
        self.pack_propagate(False)
        self._title = ctk.CTkLabel(
            self, text=title, font=Theme.FONT_H2, text_color=Theme.TEXT, anchor="w"
        )
        self._title.pack(side="left", padx=24, pady=18)

        right = ctk.CTkFrame(self, fg_color="transparent")
        right.pack(side="right", padx=24)
        ctk.CTkLabel(
            right,
            text=user_label,
            text_color=Theme.TEXT_MUTED,
            font=Theme.FONT_BODY_BOLD,
        ).pack(side="right")

    def set_title(self, text: str) -> None:
        self._title.configure(text=text)
