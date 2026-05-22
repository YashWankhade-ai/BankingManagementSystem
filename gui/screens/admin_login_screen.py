"""Admin login screen."""
from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from gui.components.buttons import GhostButton, PrimaryButton
from gui.components.cards import Card
from gui.components.dialogs import show_toast
from gui.components.forms import FormGroup
from gui.components.inputs import LabeledEntry
from gui.theme import Theme
from services.auth_service import AuthService
from utils.exceptions import AuthenticationError


class AdminLoginScreen(ctk.CTkFrame):
    def __init__(
        self,
        master,
        auth: AuthService,
        on_success: Callable[[], None],
        on_back: Callable[[], None],
    ) -> None:
        super().__init__(master, fg_color=Theme.BG)
        self._auth = auth
        self._on_success = on_success
        self._on_back = on_back
        self._build()

    def _build(self) -> None:
        card = Card(self)
        card.place(relx=0.5, rely=0.5, anchor="center")
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=44, pady=40)

        ctk.CTkLabel(
            inner, text="Administrator access", font=Theme.FONT_H1, text_color=Theme.TEXT
        ).pack(anchor="w")
        ctk.CTkLabel(
            inner,
            text="Restricted area. Authorized personnel only.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 22))

        form = FormGroup(inner)
        form.pack(fill="x")
        self._username = LabeledEntry(form, "Admin username", placeholder="admin")
        self._password = LabeledEntry(form, "Password", show="•")
        form.add(self._username)
        form.add(self._password)

        PrimaryButton(inner, text="Sign in as admin", command=self._submit, width=320).pack(pady=(8, 6))
        GhostButton(inner, text="← Back to customer login", command=self._on_back, width=320).pack()

        self._password.entry.bind("<Return>", lambda _e: self._submit())
        self._username.focus()

    def _submit(self) -> None:
        try:
            self._auth.login_admin(self._username.get(), self._password.get())
        except AuthenticationError as e:
            show_toast(self.winfo_toplevel(), str(e), "error")
            return
        show_toast(self.winfo_toplevel(), "Admin authenticated.", "success")
        self._on_success()
