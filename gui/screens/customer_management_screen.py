"""Admin customer management screen."""
from __future__ import annotations

from typing import List

import customtkinter as ctk

from gui.components.buttons import DangerButton, GhostButton, SecondaryButton
from gui.components.cards import Card
from gui.components.dialogs import ConfirmDialog, show_toast
from gui.components.inputs import LabeledEntry
from gui.components.tables import DataTable
from gui.theme import Theme
from models.account_model import Account
from models.customer_model import Customer
from repositories.account_repository import AccountRepository
from services.admin_service import AdminService
from utils.helpers import fmt_date, format_currency


class CustomerManagementScreen(ctk.CTkFrame):
    def __init__(self, master, admin_service: AdminService) -> None:
        super().__init__(master, fg_color=Theme.BG)
        self._svc = admin_service
        self._accounts_repo = AccountRepository()
        self._build()
        self._refresh("")

    def _build(self) -> None:
        wrap = ctk.CTkFrame(self, fg_color=Theme.BG)
        wrap.pack(fill="both", expand=True, padx=28, pady=20)

        header = ctk.CTkFrame(wrap, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(
            header, text="Customer management", font=Theme.FONT_H1, text_color=Theme.TEXT
        ).pack(side="left")

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right")
        self._search = LabeledEntry(right, "Search", placeholder="name, username, mobile")
        self._search.pack(side="left")
        self._search.entry.bind("<KeyRelease>", lambda _e: self._refresh(self._search.get()))

        # Customers table
        card = Card(wrap)
        card.pack(fill="both", expand=True, pady=(18, 0))
        ctk.CTkLabel(
            card, text="Customers", font=Theme.FONT_H2, text_color=Theme.TEXT
        ).pack(anchor="w", padx=22, pady=(18, 8))

        self._scroll = ctk.CTkScrollableFrame(card, fg_color=Theme.SURFACE)
        self._scroll.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _refresh(self, term: str) -> None:
        customers: List[Customer] = self._svc.search_customers(term)
        for w in self._scroll.winfo_children():
            w.destroy()

        if not customers:
            ctk.CTkLabel(
                self._scroll, text="No customers found.", text_color=Theme.TEXT_DIM
            ).pack(pady=20)
            return

        for c in customers:
            accounts: List[Account] = self._accounts_repo.by_customer(c.id)
            account = accounts[0] if accounts else None
            row = ctk.CTkFrame(
                self._scroll,
                fg_color=Theme.SURFACE_2,
                corner_radius=12,
                border_width=1,
                border_color=Theme.BORDER,
            )
            row.pack(fill="x", pady=6)

            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=18, pady=14)

            ctk.CTkLabel(
                info, text=c.full_name, text_color=Theme.TEXT, font=Theme.FONT_BODY_BOLD
            ).pack(anchor="w")
            sub = (
                f"@{c.username} · {c.mobile} · joined {fmt_date(c.created_at)}"
            )
            ctk.CTkLabel(info, text=sub, text_color=Theme.TEXT_MUTED, font=Theme.FONT_SMALL).pack(anchor="w")

            if account:
                ctk.CTkLabel(
                    info,
                    text=f"Account {account.account_number} · {account.status} · {format_currency(account.balance)}",
                    text_color=Theme.PRIMARY,
                    font=Theme.FONT_SMALL,
                ).pack(anchor="w", pady=(4, 0))

            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.pack(side="right", padx=18)

            if account:
                if account.status == "ACTIVE":
                    SecondaryButton(
                        actions,
                        text="Freeze",
                        command=lambda a=account.id: self._freeze(a),
                    ).pack(side="left", padx=6)
                else:
                    SecondaryButton(
                        actions,
                        text="Unfreeze",
                        command=lambda a=account.id: self._unfreeze(a),
                    ).pack(side="left", padx=6)

            DangerButton(
                actions,
                text="Delete",
                command=lambda cid=c.id, name=c.full_name: self._confirm_delete(cid, name),
            ).pack(side="left", padx=6)

    def _freeze(self, account_id: int) -> None:
        self._svc.freeze(account_id)
        show_toast(self.winfo_toplevel(), "Account frozen.", "warning")
        self._refresh(self._search.get())

    def _unfreeze(self, account_id: int) -> None:
        self._svc.unfreeze(account_id)
        show_toast(self.winfo_toplevel(), "Account reactivated.", "success")
        self._refresh(self._search.get())

    def _confirm_delete(self, customer_id: int, name: str) -> None:
        ConfirmDialog(
            self.winfo_toplevel(),
            title="Delete customer",
            message=f"This will permanently delete {name} and all associated accounts and transactions. This cannot be undone.",
            confirm_text="Delete",
            danger=True,
            on_confirm=lambda: self._delete(customer_id),
        )

    def _delete(self, customer_id: int) -> None:
        self._svc.delete_customer(customer_id)
        show_toast(self.winfo_toplevel(), "Customer deleted.", "success")
        self._refresh(self._search.get())
