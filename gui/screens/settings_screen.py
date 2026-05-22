"""Settings screen — change password, change PIN."""
from __future__ import annotations

import customtkinter as ctk

from gui.components.buttons import PrimaryButton
from gui.components.cards import Card
from gui.components.dialogs import show_toast
from gui.components.forms import FormGroup
from gui.components.inputs import LabeledEntry
from gui.theme import Theme
from repositories.customer_repository import CustomerRepository
from security.password_hasher import PasswordHasher
from security.pin_manager import PinManager
from services.validation_service import ValidationService
from utils.exceptions import AuthenticationError, ValidationError


class SettingsScreen(ctk.CTkFrame):
    def __init__(self, master, customer_id: int, customers: CustomerRepository) -> None:
        super().__init__(master, fg_color=Theme.BG)
        self._customer_id = customer_id
        self._customers = customers
        self._build()

    def _build(self) -> None:
        wrap = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        wrap.pack(fill="both", expand=True, padx=28, pady=20)

        ctk.CTkLabel(
            wrap, text="Settings", font=Theme.FONT_H1, text_color=Theme.TEXT
        ).pack(anchor="w")
        ctk.CTkLabel(
            wrap,
            text="Manage your security credentials.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 18))

        # Password card
        pw_card = Card(wrap)
        pw_card.pack(fill="x", pady=(0, 14))
        pw_body = ctk.CTkFrame(pw_card, fg_color="transparent")
        pw_body.pack(fill="x", padx=28, pady=24)

        ctk.CTkLabel(
            pw_body, text="Change password", font=Theme.FONT_H2, text_color=Theme.TEXT
        ).pack(anchor="w", pady=(0, 14))

        pf = FormGroup(pw_body)
        pf.pack(fill="x")
        self._pw_current = LabeledEntry(pf, "Current password", show="•")
        self._pw_new = LabeledEntry(pf, "New password", show="•")
        pf.add(self._pw_current)
        pf.add(self._pw_new)

        PrimaryButton(pw_body, text="Update password", command=self._change_password).pack(anchor="e")

        # PIN card
        pin_card = Card(wrap)
        pin_card.pack(fill="x")
        pin_body = ctk.CTkFrame(pin_card, fg_color="transparent")
        pin_body.pack(fill="x", padx=28, pady=24)

        ctk.CTkLabel(
            pin_body, text="Change PIN", font=Theme.FONT_H2, text_color=Theme.TEXT
        ).pack(anchor="w", pady=(0, 14))
        pinf = FormGroup(pin_body)
        pinf.pack(fill="x")
        self._pin_current = LabeledEntry(pinf, "Current PIN", show="•")
        self._pin_new = LabeledEntry(pinf, "New 4-digit PIN", show="•")
        pinf.add(self._pin_current)
        pinf.add(self._pin_new)

        PrimaryButton(pin_body, text="Update PIN", command=self._change_pin).pack(anchor="e")

    def _change_password(self) -> None:
        c = self._customers.by_id(self._customer_id)
        if not c:
            return
        try:
            if not PasswordHasher.verify(self._pw_current.get(), c.password_hash):
                raise AuthenticationError("Current password is incorrect.")
            new_pw = ValidationService.validate_password(self._pw_new.get())
            self._customers.update_password(c.id, PasswordHasher.hash(new_pw))
        except (AuthenticationError, ValidationError) as e:
            show_toast(self.winfo_toplevel(), str(e), "error")
            return
        show_toast(self.winfo_toplevel(), "Password updated.", "success")
        self._pw_current.set("")
        self._pw_new.set("")

    def _change_pin(self) -> None:
        c = self._customers.by_id(self._customer_id)
        if not c:
            return
        try:
            if not PinManager.verify(self._pin_current.get(), c.pin_hash):
                raise AuthenticationError("Current PIN is incorrect.")
            new_pin = ValidationService.validate_pin(self._pin_new.get())
            self._customers.update_pin(c.id, PinManager.hash(new_pin))
        except (AuthenticationError, ValidationError) as e:
            show_toast(self.winfo_toplevel(), str(e), "error")
            return
        show_toast(self.winfo_toplevel(), "PIN updated.", "success")
        self._pin_current.set("")
        self._pin_new.set("")
