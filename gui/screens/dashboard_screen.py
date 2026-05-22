"""Customer dashboard."""
from __future__ import annotations

import customtkinter as ctk

from gui.components.cards import Card, HeaderCard, StatCard
from gui.components.tables import DataTable
from gui.theme import Theme
from services.account_service import AccountService
from services.transaction_service import TransactionService
from utils.helpers import fmt_date, format_currency


class DashboardScreen(ctk.CTkFrame):
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
        self._build()

    def _build(self) -> None:
        wrap = ctk.CTkFrame(self, fg_color=Theme.BG)
        wrap.pack(fill="both", expand=True, padx=28, pady=20)

        account = self._accounts.get_customer_account(self._customer_id)
        history = self._transactions.history(account.id)
        deposits = sum(t.amount for t in history if t.type == "DEPOSIT")
        withdraws = sum(t.amount for t in history if t.type == "WITHDRAW")

        header = HeaderCard(
            wrap,
            title="Overview",
            subtitle=f"Account · {account.account_number} · Status {account.status}",
        )
        header.pack(fill="x")

        # KPI row
        kpis = ctk.CTkFrame(wrap, fg_color="transparent")
        kpis.pack(fill="x", pady=18)

        s1 = StatCard(kpis, "Available balance", format_currency(account.balance))
        s2 = StatCard(kpis, "Total deposits", format_currency(deposits), accent=Theme.SUCCESS)
        s3 = StatCard(
            kpis, "Total withdrawals", format_currency(withdraws), accent=Theme.WARNING
        )
        for w in (s1, s2, s3):
            w.pack(side="left", fill="both", expand=True, padx=8)

        # Recent activity
        recent_card = Card(wrap)
        recent_card.pack(fill="both", expand=True, pady=(6, 0))
        ctk.CTkLabel(
            recent_card,
            text="Recent activity",
            font=Theme.FONT_H2,
            text_color=Theme.TEXT,
        ).pack(anchor="w", padx=22, pady=(18, 8))

        table = DataTable(
            recent_card,
            columns=["Date", "Type", "Amount", "Balance", "Description"],
            col_widths=[180, 120, 140, 140, 240],
        )
        table.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        rows = [
            (
                fmt_date(t.created_at),
                t.type,
                format_currency(t.amount),
                format_currency(t.balance_after),
                t.description,
            )
            for t in history[:25]
        ]
        if rows:
            table.set_rows(rows)
        else:
            table.empty_state("No transactions yet — make your first deposit!")
