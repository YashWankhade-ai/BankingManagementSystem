"""Deposit screen."""
from __future__ import annotations

import customtkinter as ctk

from gui.components.buttons import PrimaryButton
from gui.components.cards import Card
from gui.components.dialogs import show_toast
from gui.components.forms import FormGroup
from gui.components.inputs import LabeledEntry
from gui.theme import Theme
from services.account_service import AccountService
from services.transaction_service import TransactionService
from utils.exceptions import BankingError
from utils.helpers import format_currency


class DepositScreen(ctk.CTkFrame):
    def __init__(
        self,
        master,
        customer_id: int,
        accounts: AccountService,
        transactions: TransactionService,
    ) -> None:
        super().__init__(master, fg_color=Theme.BG)
        self._customer_id = customer_id
        self._accounts = accounts
        self._transactions = transactions
        self._account = accounts.get_customer_account(customer_id)
        self._build()

    def _build(self) -> None:
        wrap = ctk.CTkFrame(self, fg_color=Theme.BG)
        wrap.pack(fill="both", expand=True, padx=28, pady=20)

        ctk.CTkLabel(
            wrap, text="Deposit funds", font=Theme.FONT_H1, text_color=Theme.TEXT
        ).pack(anchor="w")
        ctk.CTkLabel(
            wrap,
            text=f"Current balance · {format_currency(self._account.balance)}",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 16))

        card = Card(wrap)
        card.pack(fill="x")
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(padx=28, pady=28, fill="x")

        form = FormGroup(body)
        form.pack(fill="x")
        self._amount = LabeledEntry(form, "Amount", placeholder="100.00", width=300)
        self._desc = LabeledEntry(form, "Description (optional)", placeholder="ATM deposit")
        form.add(self._amount)
        form.add(self._desc)

        PrimaryButton(body, text="Confirm deposit", command=self._submit, width=240).pack(
            anchor="e"
        )

    def _submit(self) -> None:
        try:
            new_balance = self._transactions.deposit(
                self._account.id,
                self._amount.get(),
                description=self._desc.get() or "Deposit",
            )
        except BankingError as e:
            show_toast(self.winfo_toplevel(), str(e), "error")
            return
        except Exception as e:  # noqa: BLE001
            show_toast(self.winfo_toplevel(), f"Deposit failed: {e}", "error")
            return
        show_toast(
            self.winfo_toplevel(),
            f"Deposited. New balance: {format_currency(new_balance)}",
            "success",
        )
        self._amount.set("")
        self._desc.set("")
        self._account = self._accounts.get_customer_account(self._customer_id)
