"""Sidebar navigation."""
from __future__ import annotations

from typing import Callable, List, Tuple

import customtkinter as ctk

from gui.theme import Theme


class Sidebar(ctk.CTkFrame):
    def __init__(
        self,
        master,
        items: List[Tuple[str, str, str]],  # (key, label, icon_text)
        on_select: Callable[[str], None],
        on_logout: Callable[[], None],
        title: str = "NovaBank",
        subtitle: str = "",
    ) -> None:
        super().__init__(master, width=250, corner_radius=0, fg_color=Theme.SIDEBAR_BG)
        self.pack_propagate(False)
        self._on_select = on_select
        self._buttons: dict[str, ctk.CTkButton] = {}

        # Brand
        brand = ctk.CTkFrame(self, fg_color="transparent")
        brand.pack(fill="x", padx=22, pady=(28, 6))
        ctk.CTkLabel(
            brand,
            text="◆ " + title,
            text_color=Theme.TEXT,
            font=("Segoe UI", 20, "bold"),
            anchor="w",
        ).pack(fill="x")
        if subtitle:
            ctk.CTkLabel(
                brand,
                text=subtitle,
                text_color=Theme.TEXT_DIM,
                font=Theme.FONT_SMALL,
                anchor="w",
            ).pack(fill="x", pady=(2, 0))

        sep = ctk.CTkFrame(self, height=1, fg_color=Theme.BORDER)
        sep.pack(fill="x", padx=18, pady=18)

        # Nav items
        for key, label, icon in items:
            btn = ctk.CTkButton(
                self,
                text=f"  {icon}   {label}",
                command=lambda k=key: self._select(k),
                anchor="w",
                height=42,
                corner_radius=10,
                fg_color="transparent",
                hover_color=Theme.SIDEBAR_ACTIVE,
                text_color=Theme.TEXT_MUTED,
                font=Theme.FONT_BODY_BOLD,
            )
            btn.pack(fill="x", padx=14, pady=3)
            self._buttons[key] = btn

        # Logout pinned bottom
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        ctk.CTkButton(
            self,
            text="  ⎋   Sign out",
            command=on_logout,
            anchor="w",
            height=42,
            corner_radius=10,
            fg_color="transparent",
            hover_color=Theme.SURFACE_3,
            text_color=Theme.DANGER,
            font=Theme.FONT_BODY_BOLD,
        ).pack(fill="x", padx=14, pady=(0, 18))

    def _select(self, key: str) -> None:
        self.set_active(key)
        self._on_select(key)

    def set_active(self, key: str) -> None:
        for k, btn in self._buttons.items():
            if k == key:
                btn.configure(fg_color=Theme.SIDEBAR_ACTIVE, text_color=Theme.TEXT)
            else:
                btn.configure(fg_color="transparent", text_color=Theme.TEXT_MUTED)
