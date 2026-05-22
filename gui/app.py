"""Top-level CTk application shell."""
from __future__ import annotations

import customtkinter as ctk

from config import CONFIG
from gui.components.dialogs import show_toast
from gui.navigation.navigation_manager import NavigationManager
from gui.navigation.sidebar import Sidebar
from gui.navigation.topbar import TopBar
from gui.screens.admin_login_screen import AdminLoginScreen
from gui.screens.balance_screen import BalanceScreen
from gui.screens.create_account_screen import CreateAccountScreen
from gui.screens.customer_management_screen import CustomerManagementScreen
from gui.screens.dashboard_screen import DashboardScreen
from gui.screens.deposit_screen import DepositScreen
from gui.screens.login_screen import LoginScreen
from gui.screens.settings_screen import SettingsScreen
from gui.screens.transaction_history_screen import TransactionHistoryScreen
from gui.screens.withdraw_screen import WithdrawScreen
from gui.theme import Theme
from repositories.customer_repository import CustomerRepository
from security.session_manager import SessionManager
from services.account_service import AccountService
from services.admin_service import AdminService
from services.auth_service import AuthService
from services.transaction_service import TransactionService
from utils.constants import ROLE_ADMIN, ROLE_CUSTOMER
from utils.logger import get_logger

logger = get_logger(__name__)


class BankingApp(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode(CONFIG.APPEARANCE_MODE)
        ctk.set_default_color_theme("blue")

        self.title(CONFIG.APP_NAME)
        self.geometry(f"{CONFIG.WINDOW_WIDTH}x{CONFIG.WINDOW_HEIGHT}")
        self.minsize(1100, 720)
        self.configure(fg_color=Theme.BG)

        # Services (DI container — single shared instance)
        self._sessions = SessionManager.instance()
        self._customers_repo = CustomerRepository()
        self._auth = AuthService(sessions=self._sessions)
        self._accounts = AccountService()
        self._transactions = TransactionService()
        self._admin_service = AdminService()

        self._root_container = ctk.CTkFrame(self, fg_color=Theme.BG)
        self._root_container.pack(fill="both", expand=True)

        self._show_login()

    # =================================================================
    # Auth flow shells
    # =================================================================
    def _clear_root(self) -> None:
        for w in self._root_container.winfo_children():
            w.destroy()

    def _show_login(self) -> None:
        self._clear_root()
        screen = LoginScreen(
            self._root_container,
            auth=self._auth,
            on_success=self._show_customer_shell,
            on_create_account=self._show_create_account,
            on_admin_login=self._show_admin_login,
        )
        screen.pack(fill="both", expand=True)

    def _show_admin_login(self) -> None:
        self._clear_root()
        screen = AdminLoginScreen(
            self._root_container,
            auth=self._auth,
            on_success=self._show_admin_shell,
            on_back=self._show_login,
        )
        screen.pack(fill="both", expand=True)

    def _show_create_account(self) -> None:
        self._clear_root()
        screen = CreateAccountScreen(
            self._root_container,
            accounts=self._accounts,
            on_back=self._show_login,
            on_created=lambda _acc: self._show_login(),
        )
        screen.pack(fill="both", expand=True)

    # =================================================================
    # Authenticated shells (sidebar + content)
    # =================================================================
    def _build_shell(self, items, default_key: str, screen_factory) -> None:
        self._clear_root()
        session = self._sessions.current
        if not session:
            self._show_login()
            return

        sidebar = Sidebar(
            self._root_container,
            items=items,
            on_select=lambda key: self._navigate(key),
            on_logout=self._logout,
            title="NovaBank",
            subtitle=f"Signed in as {session.username}",
        )
        sidebar.pack(side="left", fill="y")

        right = ctk.CTkFrame(self._root_container, fg_color=Theme.BG)
        right.pack(side="left", fill="both", expand=True)

        self._topbar = TopBar(right, title="Dashboard", user_label=f"● {session.username}")
        self._topbar.pack(fill="x")

        content = ctk.CTkFrame(right, fg_color=Theme.BG)
        content.pack(fill="both", expand=True)

        self._sidebar = sidebar
        self._nav = NavigationManager(content)
        self._screen_factory = screen_factory
        screen_factory(self._nav)

        self._navigate(default_key)

    def _navigate(self, key: str) -> None:
        title_map = {
            "dashboard": "Dashboard",
            "deposit": "Deposit",
            "withdraw": "Withdraw",
            "balance": "Balance enquiry",
            "history": "Transaction history",
            "settings": "Settings",
            "admin_dashboard": "Admin overview",
            "customers": "Customer management",
            "all_transactions": "All transactions",
        }
        try:
            self._nav.navigate(key)
        except KeyError:
            show_toast(self, "Screen not found", "error")
            return
        self._sidebar.set_active(key)
        self._topbar.set_title(title_map.get(key, "NovaBank"))

    # ----- customer shell ---------------------------------------------
    def _show_customer_shell(self) -> None:
        session = self._sessions.current
        if not session or session.role != ROLE_CUSTOMER:
            self._show_login()
            return

        cid = session.user_id

        def register(nav: NavigationManager) -> None:
            nav.register("dashboard", lambda parent: DashboardScreen(parent, cid, self._accounts, self._transactions))
            nav.register("deposit", lambda parent: DepositScreen(parent, cid, self._accounts, self._transactions))
            nav.register("withdraw", lambda parent: WithdrawScreen(parent, cid, self._accounts, self._transactions))
            nav.register("balance", lambda parent: BalanceScreen(parent, cid, self._accounts, self._customers_repo))
            nav.register("history", lambda parent: TransactionHistoryScreen(parent, cid, self._accounts, self._transactions))
            nav.register("settings", lambda parent: SettingsScreen(parent, cid, self._customers_repo))

        items = [
            ("dashboard", "Dashboard", "▣"),
            ("deposit", "Deposit", "↓"),
            ("withdraw", "Withdraw", "↑"),
            ("balance", "Balance", "$"),
            ("history", "History", "≡"),
            ("settings", "Settings", "⚙"),
        ]
        self._build_shell(items, "dashboard", register)

    # ----- admin shell ------------------------------------------------
    def _show_admin_shell(self) -> None:
        session = self._sessions.current
        if not session or session.role != ROLE_ADMIN:
            self._show_login()
            return

        from gui.components.cards import HeaderCard, StatCard
        from gui.components.tables import DataTable
        from utils.helpers import fmt_date, format_currency

        admin_service = self._admin_service

        def admin_dashboard(parent: ctk.CTkFrame) -> ctk.CTkFrame:
            wrap = ctk.CTkFrame(parent, fg_color=Theme.BG)
            inner = ctk.CTkFrame(wrap, fg_color=Theme.BG)
            inner.pack(fill="both", expand=True, padx=28, pady=20)

            customers = admin_service.search_customers("")
            accounts = admin_service.all_accounts()
            txs = admin_service.all_transactions()
            total = sum(a.balance for a in accounts)

            HeaderCard(
                inner,
                title="Administrator overview",
                subtitle="System-wide metrics and activity.",
            ).pack(fill="x")

            kpis = ctk.CTkFrame(inner, fg_color="transparent")
            kpis.pack(fill="x", pady=18)
            for w in (
                StatCard(kpis, "Customers", str(len(customers))),
                StatCard(kpis, "Accounts", str(len(accounts)), accent=Theme.ACCENT),
                StatCard(kpis, "Total deposits held", format_currency(total), accent=Theme.SUCCESS),
                StatCard(kpis, "Transactions", str(len(txs)), accent=Theme.WARNING),
            ):
                w.pack(side="left", fill="both", expand=True, padx=8)

            table = DataTable(
                inner,
                columns=["Date", "Account", "Type", "Amount", "Balance after"],
                col_widths=[180, 90, 120, 140, 160],
            )
            table.pack(fill="both", expand=True, pady=(6, 0))
            rows = [
                (fmt_date(t.created_at), str(t.account_id), t.type,
                 format_currency(t.amount), format_currency(t.balance_after))
                for t in txs[:50]
            ]
            if rows:
                table.set_rows(rows)
            else:
                table.empty_state("No transactions yet.")

            return wrap

        def all_transactions(parent: ctk.CTkFrame) -> ctk.CTkFrame:
            wrap = ctk.CTkFrame(parent, fg_color=Theme.BG)
            inner = ctk.CTkFrame(wrap, fg_color=Theme.BG)
            inner.pack(fill="both", expand=True, padx=28, pady=20)
            ctk.CTkLabel(
                inner, text="All transactions", font=Theme.FONT_H1, text_color=Theme.TEXT
            ).pack(anchor="w")
            ctk.CTkLabel(
                inner,
                text="Most recent 500 transactions across all accounts.",
                font=Theme.FONT_BODY,
                text_color=Theme.TEXT_MUTED,
            ).pack(anchor="w", pady=(2, 14))
            table = DataTable(
                inner,
                columns=["Date", "Account", "Type", "Amount", "Balance", "Description"],
                col_widths=[180, 90, 120, 140, 140, 220],
            )
            table.pack(fill="both", expand=True)
            txs = admin_service.all_transactions()
            rows = [
                (
                    fmt_date(t.created_at),
                    str(t.account_id),
                    t.type,
                    format_currency(t.amount),
                    format_currency(t.balance_after),
                    t.description,
                )
                for t in txs
            ]
            if rows:
                table.set_rows(rows)
            else:
                table.empty_state("No transactions yet.")
            return wrap

        def register(nav: NavigationManager) -> None:
            nav.register("admin_dashboard", admin_dashboard)
            nav.register("customers", lambda parent: CustomerManagementScreen(parent, admin_service))
            nav.register("all_transactions", all_transactions)

        items = [
            ("admin_dashboard", "Overview", "▣"),
            ("customers", "Customers", "◉"),
            ("all_transactions", "Transactions", "≡"),
        ]
        self._build_shell(items, "admin_dashboard", register)

    # ------------------------------------------------------------------
    def _logout(self) -> None:
        self._auth.logout()
        show_toast(self, "Signed out.", "info")
        self._show_login()
