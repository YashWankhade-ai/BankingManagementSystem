"""Toast notifications & confirmation dialogs."""
from __future__ import annotations

import threading
from typing import Callable, Optional

import customtkinter as ctk

from gui.theme import Theme


class Toast(ctk.CTkToplevel):
    """Auto-dismissing notification at the bottom of the screen."""

    _COLORS = {
        "success": Theme.SUCCESS,
        "error": Theme.DANGER,
        "info": Theme.PRIMARY,
        "warning": Theme.WARNING,
    }

    def __init__(self, master, message: str, kind: str = "info", duration_ms: int = 2500) -> None:
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color=Theme.SURFACE_2)
        try:
            self.attributes("-alpha", 0.97)
        except Exception:
            pass

        accent = self._COLORS.get(kind, Theme.PRIMARY)
        bar = ctk.CTkFrame(self, width=4, fg_color=accent, corner_radius=0)
        bar.pack(side="left", fill="y")
        ctk.CTkLabel(
            self, text=message, text_color=Theme.TEXT, font=Theme.FONT_BODY_BOLD
        ).pack(side="left", padx=18, pady=14)

        self.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        sw = master.winfo_screenwidth()
        sh = master.winfo_screenheight()
        x = (sw - w) // 2
        y = sh - h - 80
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.after(duration_ms, self.destroy)


def show_toast(master, message: str, kind: str = "info") -> None:
    Toast(master, message, kind)


class ConfirmDialog(ctk.CTkToplevel):
    """Modal yes/no confirmation."""

    def __init__(
        self,
        master,
        title: str,
        message: str,
        on_confirm: Callable[[], None],
        confirm_text: str = "Confirm",
        danger: bool = False,
    ) -> None:
        super().__init__(master)
        self.title(title)
        self.configure(fg_color=Theme.SURFACE)
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self.geometry("420x200")
        self._center(master)

        ctk.CTkLabel(
            self, text=title, font=Theme.FONT_H2, text_color=Theme.TEXT
        ).pack(pady=(20, 6), padx=24, anchor="w")
        ctk.CTkLabel(
            self,
            text=message,
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
            wraplength=360,
            justify="left",
        ).pack(padx=24, anchor="w")

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", side="bottom", padx=24, pady=18)

        from gui.components.buttons import DangerButton, PrimaryButton, SecondaryButton

        SecondaryButton(btns, text="Cancel", command=self.destroy).pack(side="right", padx=(8, 0))
        confirm_cls = DangerButton if danger else PrimaryButton
        confirm_cls(
            btns,
            text=confirm_text,
            command=lambda: (on_confirm(), self.destroy()),
        ).pack(side="right")

    def _center(self, master) -> None:
        self.update_idletasks()
        try:
            mx = master.winfo_rootx()
            my = master.winfo_rooty()
            mw = master.winfo_width()
            mh = master.winfo_height()
            w = self.winfo_width()
            h = self.winfo_height()
            self.geometry(f"+{mx + (mw - w) // 2}+{my + (mh - h) // 2}")
        except Exception:
            pass
