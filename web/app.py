"""Flask web application for NovaBank."""
from __future__ import annotations

import os
from functools import wraps
from pathlib import Path
from typing import Any, Callable

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from config import CONFIG
from database.migrations import run_migrations
from repositories.account_repository import AccountRepository
from repositories.customer_repository import CustomerRepository
from repositories.transaction_repository import TransactionRepository
from services.account_service import AccountService
from services.admin_service import AdminService
from services.auth_service import AuthService
from services.transaction_service import TransactionService
from utils.exceptions import BankingError
from utils.logger import get_logger

logger = get_logger("web")


def customer_required(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if "customer_id" not in session:
            flash("Please sign in to access your banking dashboard.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if "admin_id" not in session:
            flash("Admin authentication required.", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function


def create_web_app() -> Flask:
    template_dir = str(Path(__file__).parent / "templates")
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = os.environ.get("SECRET_KEY", "novabank-super-secret-key-2026")

    # Ensure database migrations have run
    try:
        run_migrations()
    except Exception as e:
        logger.warning("Migration on startup warning: %s", e)

    # Initialize services
    customers_repo = CustomerRepository()
    accounts_repo = AccountRepository()
    tx_repo = TransactionRepository()

    auth_service = AuthService(customers=customers_repo)
    account_service = AccountService(customers=customers_repo, accounts=accounts_repo)
    tx_service = TransactionService(accounts=accounts_repo, customers=customers_repo, transactions=tx_repo)
    admin_service = AdminService(customers=customers_repo, accounts=accounts_repo, transactions=tx_repo)

    @app.route("/healthz")
    def healthz() -> str:
        return "OK"

    # ------------------------------------------------------------- Customer Auth
    @app.route("/login", methods=["GET", "POST"])
    def login() -> Any:
        if "customer_id" in session:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            try:
                customer = auth_service.login_customer(username, password)
                session["customer_id"] = customer.id
                session["username"] = customer.username
                session["customer_name"] = customer.full_name
                flash(f"Welcome back, {customer.full_name}!", "success")
                return redirect(url_for("dashboard"))
            except BankingError as e:
                flash(str(e), "error")
            except Exception as e:
                logger.exception("Login error: %s", e)
                flash("Login failed. Please check your credentials.", "error")

        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register() -> Any:
        if request.method == "POST":
            full_name = request.form.get("full_name", "").strip()
            dob = request.form.get("dob", "").strip()
            mobile = request.form.get("mobile", "").strip()
            address = request.form.get("address", "").strip()
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            pin = request.form.get("pin", "").strip()
            deposit_raw = request.form.get("initial_deposit", "0")

            try:
                deposit = float(deposit_raw or 0)
                customer, account = account_service.register_customer(
                    full_name=full_name,
                    dob=dob,
                    mobile=mobile,
                    address=address,
                    username=username,
                    password=password,
                    pin=pin,
                    initial_deposit=deposit,
                )
                session["customer_id"] = customer.id
                session["username"] = customer.username
                session["customer_name"] = customer.full_name
                flash(f"Account opened successfully! Your account number is {account.account_number}.", "success")
                return redirect(url_for("dashboard"))
            except BankingError as e:
                flash(str(e), "error")
            except Exception as e:
                logger.exception("Registration error: %s", e)
                flash(f"Registration failed: {e}", "error")

        return render_template("register.html")

    @app.route("/logout")
    def logout() -> Any:
        session.clear()
        flash("You have been signed out.", "success")
        return redirect(url_for("login"))

    # ------------------------------------------------------------- Customer Portal
    @app.route("/")
    @customer_required
    def dashboard() -> Any:
        customer_id = session["customer_id"]
        customer = customers_repo.by_id(customer_id)
        if not customer:
            session.clear()
            return redirect(url_for("login"))

        account = account_service.get_customer_account(customer_id)
        transactions = tx_service.history(account.id)[:5]
        return render_template("dashboard.html", customer=customer, account=account, transactions=transactions)

    @app.route("/deposit", methods=["GET", "POST"])
    @customer_required
    def deposit() -> Any:
        customer_id = session["customer_id"]
        account = account_service.get_customer_account(customer_id)

        if request.method == "POST":
            amount_raw = request.form.get("amount", "0")
            description = request.form.get("description", "").strip() or "Web Deposit"
            try:
                amount = float(amount_raw)
                new_balance = tx_service.deposit(account.id, amount, description)
                flash(f"Successfully deposited ₹{amount:,.2f}. New balance: ₹{new_balance:,.2f}", "success")
                return redirect(url_for("dashboard"))
            except BankingError as e:
                flash(str(e), "error")
            except Exception as e:
                flash(f"Deposit failed: {e}", "error")

        return render_template("deposit.html", account=account)

    @app.route("/withdraw", methods=["GET", "POST"])
    @customer_required
    def withdraw() -> Any:
        customer_id = session["customer_id"]
        account = account_service.get_customer_account(customer_id)

        if request.method == "POST":
            amount_raw = request.form.get("amount", "0")
            pin = request.form.get("pin", "").strip()
            description = request.form.get("description", "").strip() or "Web Withdrawal"
            try:
                amount = float(amount_raw)
                new_balance = tx_service.withdraw(
                    account_id=account.id,
                    amount=amount,
                    pin=pin,
                    description=description,
                )
                flash(f"Successfully withdrew ₹{amount:,.2f}. Remaining balance: ₹{new_balance:,.2f}", "success")
                return redirect(url_for("dashboard"))
            except BankingError as e:
                flash(str(e), "error")
            except Exception as e:
                flash(f"Withdrawal failed: {e}", "error")

        return render_template("withdraw.html", account=account)

    @app.route("/transactions")
    @customer_required
    def transactions() -> Any:
        customer_id = session["customer_id"]
        account = account_service.get_customer_account(customer_id)
        query = request.args.get("q", "").strip()
        tx_list = tx_service.history(account.id, search=query)
        return render_template("transactions.html", account=account, transactions=tx_list, query=query)

    # ------------------------------------------------------------- Admin Portal
    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login() -> Any:
        if "admin_id" in session:
            return redirect(url_for("admin_dashboard"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            try:
                admin = auth_service.login_admin(username, password)
                session["admin_id"] = admin.id
                session["admin_username"] = admin.username
                flash("Admin authenticated successfully.", "success")
                return redirect(url_for("admin_dashboard"))
            except BankingError as e:
                flash(str(e), "error")
            except Exception as e:
                flash("Admin login failed.", "error")

        return render_template("admin_login.html")

    @app.route("/admin")
    @admin_required
    def admin_dashboard() -> Any:
        query = request.args.get("q", "").strip()
        customers = admin_service.search_customers(query)
        accounts = admin_service.all_accounts()
        all_tx = admin_service.all_transactions()

        # Map customer_id -> account
        customer_accounts = {acc.customer_id: acc for acc in accounts}
        total_deposits = sum(acc.balance for acc in accounts)

        return render_template(
            "admin_dashboard.html",
            customers=customers,
            accounts=accounts,
            customer_accounts=customer_accounts,
            total_deposits=total_deposits,
            total_transactions=len(all_tx),
            query=query,
        )

    @app.route("/admin/freeze/<int:account_id>", methods=["POST"])
    @admin_required
    def admin_freeze(account_id: int) -> Any:
        try:
            admin_service.freeze(account_id)
            flash(f"Account #{account_id} has been frozen.", "success")
        except Exception as e:
            flash(f"Failed to freeze account: {e}", "error")
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/unfreeze/<int:account_id>", methods=["POST"])
    @admin_required
    def admin_unfreeze(account_id: int) -> Any:
        try:
            admin_service.unfreeze(account_id)
            flash(f"Account #{account_id} has been unfrozen.", "success")
        except Exception as e:
            flash(f"Failed to unfreeze account: {e}", "error")
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/delete/<int:customer_id>", methods=["POST"])
    @admin_required
    def admin_delete(customer_id: int) -> Any:
        try:
            admin_service.delete_customer(customer_id)
            flash("Customer deleted successfully.", "success")
        except Exception as e:
            flash(f"Failed to delete customer: {e}", "error")
        return redirect(url_for("admin_dashboard"))

    @app.route("/admin/logout")
    def admin_logout() -> Any:
        session.clear()
        flash("Admin session terminated.", "success")
        return redirect(url_for("admin_login"))

    return app
