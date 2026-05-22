"""Balance enquiry screen."""
from __future__ import annotations

import customtkinter as ctk

from gui.components.cards import Card, StatCard
from gui.theme import Theme
from repositories.customer_repository import CustomerRepository
from services.account_service import AccountService
from utils.helpers import fmt_date, format_currency


class BalanceScreen(ctk.CTkFrame):
    def __init__(
        self,
        master,
        customer_id: int,
        accounts: AccountService,
        customers: CustomerRepository,
    ) -> None:
        super().__init__(master, fg_color=Theme.BG)
        self._customer_id = customer_id
        self._accounts = accounts
        self._customers = customers
        self._build()

    def _build(self) -> None:
        wrap = ctk.CTkFrame(self, fg_color=Theme.BG)
        wrap.pack(fill="both", expand=True, padx=28, pady=20)

        account = self._accounts.get_customer_account(self._customer_id)
        customer = self._customers.by_id(self._customer_id)

        ctk.CTkLabel(
            wrap, text="Balance enquiry", font=Theme.FONT_H1, text_color=Theme.TEXT
        ).pack(anchor="w")
        ctk.CTkLabel(
            wrap,
            text="Your real-time account snapshot.",
            font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", pady=(2, 18))

        StatCard(wrap, "Available balance", format_currency(account.balance)).pack(
            fill="x", pady=(0, 14)
        )

        details = Card(wrap)
        details.pack(fill="x")
        inner = ctk.CTkFrame(details, fg_color="transparent")
        inner.pack(fill="x", padx=24, pady=22)

        rows = [
            ("Account holder", customer.full_name if customer else "—"),
            ("Account number", account.account_number),
            ("Status", account.status),
            ("Username", customer.username if customer else "—"),
            ("Mobile", customer.mobile if customer else "—"),
            ("Opened", fmt_date(account.created_at)),
            ("Last updated", fmt_date(account.updated_at)),
        ]
        for label, value in rows:
            row = ctk.CTkFrame(inner, fg_color="transparent")
            row.pack(fill="x", pady=6)
            ctk.CTkLabel(
                row,
                text=label,
                width=180,
                anchor="w",
                text_color=Theme.TEXT_MUTED,
                font=Theme.FONT_BODY,
            ).pack(side="left")
            ctk.CTkLabel(
                row,
                text=value,
                anchor="w",
                text_color=Theme.TEXT,
                font=Theme.FONT_BODY_BOLD,
            ).pack(side="left")
