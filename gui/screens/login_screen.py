"""Customer login screen."""
from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from gui.components.buttons import GhostButton, PrimaryButton, SecondaryButton
from gui.components.cards import Card
from gui.components.dialogs import show_toast
from gui.components.forms import FormGroup
from gui.components.inputs import LabeledEntry
from gui.theme import Theme
from services.auth_service import AuthService
from utils.exceptions import AuthenticationError


class LoginScreen(ctk.CTkFrame):
    def __init__(
        self,
        master,
        auth: AuthService,
        on_success: Callable[[], None],
        on_create_account: Callable[[], None],
        on_admin_login: Callable[[], None],
    ) -> None:
        super().__init__(master, fg_color=Theme.BG)
        self._auth = auth
        self._on_success = on_success
        self._on_create_account = on_create_account
        self._on_admin_login = on_admin_login

        self._build()

    # ------------------------------------------------------------------
    def _build(self) -> None:
        # Two-column hero layout
        left = ctk.CTkFrame(self, fg_color=Theme.BG)
        left.pack(side="left", fill="both", expand=True)
        right = ctk.CTkFrame(self, fg_color=Theme.SURFACE)
        right.pack(side="right", fill="both", expand=True)

        # Brand panel
        brand = ctk.CTkFrame(left, fg_color="transparent")
        brand.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(
            brand, text="◆ NovaBank", text_color=Theme.TEXT, font=("Segoe UI", 36, "bold")
        ).pack(anchor="w")
        ctk.CTkLabel(
            brand,
            text="Enterprise Banking, Reimagined.",
            text_color=Theme.PRIMARY,
            font=Theme.FONT_H2,
        ).pack(anchor="w", pady=(6, 18))
        ctk.CTkLabel(
            brand,
            text="Secure accounts · Instant transfers · Real-time insights\n"
                 "Trusted by enterprises worldwide.",
            text_color=Theme.TEXT_MUTED,
            font=Theme.FONT_BODY,
            justify="left",
        ).pack(anchor="w")

        # Form
        card = Card(right)
        card.place(relx=0.5, rely=0.5, anchor="center")
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=44, pady=40)

        ctk.CTkLabel(
            inner, text="Welcome back", font=Theme.FONT_H1, text_color=Theme.TEXT
        ).pack(anchor="w")
        ctk.CTkLabel(
            inner,
            text="Sign in to your NovaBank account.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 22))

        form = FormGroup(inner)
        form.pack(fill="x")
        self._username = LabeledEntry(form, "Username", placeholder="e.g. jane.doe")
        self._password = LabeledEntry(form, "Password", placeholder="••••••••", show="•")
        form.add(self._username)
        form.add(self._password)

        PrimaryButton(inner, text="Sign in", command=self._submit, width=320).pack(pady=(8, 8))
        SecondaryButton(
            inner, text="Create new account", command=self._on_create_account, width=320
        ).pack()
        GhostButton(
            inner, text="Sign in as administrator", command=self._on_admin_login, width=320
        ).pack(pady=(14, 0))

        self._password.entry.bind("<Return>", lambda _e: self._submit())
        self._username.focus()

    # ------------------------------------------------------------------
    def _submit(self) -> None:
        try:
            self._auth.login_customer(self._username.get(), self._password.get())
        except AuthenticationError as e:
            show_toast(self.winfo_toplevel(), str(e), "error")
            return
        except Exception as e:  # noqa: BLE001
            show_toast(self.winfo_toplevel(), f"Login failed: {e}", "error")
            return
        show_toast(self.winfo_toplevel(), "Welcome back!", "success")
        self._on_success()
