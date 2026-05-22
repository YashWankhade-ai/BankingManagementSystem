"""Customer registration screen."""
from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from gui.components.buttons import GhostButton, PrimaryButton
from gui.components.cards import Card
from gui.components.dialogs import show_toast
from gui.components.forms import FormGroup
from gui.components.inputs import LabeledEntry, LabeledTextarea
from gui.theme import Theme
from services.account_service import AccountService
from utils.exceptions import BankingError


class CreateAccountScreen(ctk.CTkFrame):
    def __init__(
        self,
        master,
        accounts: AccountService,
        on_back: Callable[[], None],
        on_created: Callable[[str], None],
    ) -> None:
        super().__init__(master, fg_color=Theme.BG)
        self._accounts = accounts
        self._on_back = on_back
        self._on_created = on_created
        self._build()

    def _build(self) -> None:
        wrap = ctk.CTkScrollableFrame(self, fg_color=Theme.BG)
        wrap.pack(fill="both", expand=True, padx=40, pady=24)

        ctk.CTkLabel(
            wrap, text="Open a new account", font=Theme.FONT_H1, text_color=Theme.TEXT
        ).pack(anchor="w")
        ctk.CTkLabel(
            wrap,
            text="Your information is encrypted and stored securely.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 18))

        card = Card(wrap)
        card.pack(fill="x", pady=10)
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(padx=28, pady=28, fill="x")

        # Two-column grid
        cols = ctk.CTkFrame(body, fg_color="transparent")
        cols.pack(fill="x")
        left = FormGroup(cols)
        right = FormGroup(cols)
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))
        right.pack(side="left", fill="both", expand=True, padx=(14, 0))

        self._full_name = LabeledEntry(left, "Full name", placeholder="Jane Doe")
        self._dob = LabeledEntry(left, "Date of birth", placeholder="YYYY-MM-DD")
        self._mobile = LabeledEntry(left, "Mobile", placeholder="+15551234567")
        self._username = LabeledEntry(left, "Username", placeholder="jane.doe")

        self._password = LabeledEntry(right, "Password", show="•")
        self._pin = LabeledEntry(right, "4-digit PIN", show="•")
        self._deposit = LabeledEntry(right, "Initial deposit", placeholder="0.00")
        self._address = LabeledTextarea(right, "Address")

        for w in (self._full_name, self._dob, self._mobile, self._username):
            left.add(w)
        for w in (self._password, self._pin, self._deposit, self._address):
            right.add(w)

        actions = ctk.CTkFrame(body, fg_color="transparent")
        actions.pack(fill="x", pady=(8, 0))
        GhostButton(actions, text="← Back", command=self._on_back).pack(side="left")
        PrimaryButton(actions, text="Open account", command=self._submit).pack(side="right")

    def _submit(self) -> None:
        try:
            deposit_str = (self._deposit.get() or "0").strip() or "0"
            customer, account = self._accounts.register_customer(
                full_name=self._full_name.get(),
                dob=self._dob.get(),
                mobile=self._mobile.get(),
                address=self._address.get(),
                username=self._username.get(),
                password=self._password.get(),
                pin=self._pin.get(),
                initial_deposit=float(deposit_str),
            )
        except BankingError as e:
            show_toast(self.winfo_toplevel(), str(e), "error")
            return
        except ValueError:
            show_toast(self.winfo_toplevel(), "Initial deposit must be a number.", "error")
            return
        except Exception as e:  # noqa: BLE001
            show_toast(self.winfo_toplevel(), f"Could not create account: {e}", "error")
            return

        show_toast(
            self.winfo_toplevel(),
            f"Account opened · {account.account_number}",
            "success",
        )
        self._on_created(account.account_number)
