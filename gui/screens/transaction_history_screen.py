"""Transaction history screen."""
from __future__ import annotations

import customtkinter as ctk

from gui.components.cards import Card
from gui.components.inputs import LabeledEntry
from gui.components.tables import DataTable
from gui.theme import Theme
from services.account_service import AccountService
from services.transaction_service import TransactionService
from utils.helpers import fmt_date, format_currency


class TransactionHistoryScreen(ctk.CTkFrame):
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
        self._refresh("")

    def _build(self) -> None:
        wrap = ctk.CTkFrame(self, fg_color=Theme.BG)
        wrap.pack(fill="both", expand=True, padx=28, pady=20)

        header = ctk.CTkFrame(wrap, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text="Transaction history",
            font=Theme.FONT_H1,
            text_color=Theme.TEXT,
        ).pack(side="left")

        # Search
        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right")
        self._search = LabeledEntry(right, "Search", placeholder="Type or description")
        self._search.pack(side="left")
        self._search.entry.bind("<KeyRelease>", lambda _e: self._refresh(self._search.get()))

        card = Card(wrap)
        card.pack(fill="both", expand=True, pady=(18, 0))

        self._table = DataTable(
            card,
            columns=["Date", "Type", "Amount", "Balance", "Description"],
            col_widths=[180, 120, 140, 140, 280],
        )
        self._table.pack(fill="both", expand=True, padx=18, pady=18)

    def _refresh(self, term: str) -> None:
        history = self._transactions.history(self._account.id, term)
        rows = [
            (
                fmt_date(t.created_at),
                t.type,
                format_currency(t.amount),
                format_currency(t.balance_after),
                t.description,
            )
            for t in history
        ]
        if rows:
            self._table.set_rows(rows)
        else:
            self._table.empty_state("No matching transactions.")
