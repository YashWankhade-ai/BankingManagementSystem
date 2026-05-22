"""Centralized SQL constants. Keeps SQL out of business logic."""
from __future__ import annotations


class CustomerQ:
    INSERT = (
        "INSERT INTO customers(full_name, dob, mobile, address, username, "
        "password_hash, pin_hash) VALUES(?,?,?,?,?,?,?)"
    )
    BY_ID = "SELECT * FROM customers WHERE id = ?"
    BY_USERNAME = "SELECT * FROM customers WHERE username = ?"
    ALL = "SELECT * FROM customers ORDER BY id DESC"
    DELETE = "DELETE FROM customers WHERE id = ?"
    UPDATE_PIN = "UPDATE customers SET pin_hash = ?, updated_at = datetime('now') WHERE id = ?"
    UPDATE_PASSWORD = (
        "UPDATE customers SET password_hash = ?, updated_at = datetime('now') WHERE id = ?"
    )


class AccountQ:
    INSERT = (
        "INSERT INTO accounts(account_number, customer_id, balance, status) "
        "VALUES(?,?,?, 'ACTIVE')"
    )
    BY_ID = "SELECT * FROM accounts WHERE id = ?"
    BY_NUMBER = "SELECT * FROM accounts WHERE account_number = ?"
    BY_CUSTOMER = "SELECT * FROM accounts WHERE customer_id = ?"
    ALL = "SELECT * FROM accounts ORDER BY id DESC"
    UPDATE_BALANCE = (
        "UPDATE accounts SET balance = ?, updated_at = datetime('now') WHERE id = ?"
    )
    UPDATE_STATUS = (
        "UPDATE accounts SET status = ?, updated_at = datetime('now') WHERE id = ?"
    )
    DELETE = "DELETE FROM accounts WHERE id = ?"


class AdminQ:
    BY_USERNAME = "SELECT * FROM admins WHERE username = ?"
    INSERT = "INSERT INTO admins(username, password_hash, role) VALUES(?,?,?)"


class TransactionQ:
    INSERT = (
        "INSERT INTO transactions(account_id, type, amount, balance_after, description) "
        "VALUES(?,?,?,?,?)"
    )
    BY_ACCOUNT = (
        "SELECT * FROM transactions WHERE account_id = ? ORDER BY created_at DESC"
    )
    SEARCH = (
        "SELECT * FROM transactions WHERE account_id = ? AND "
        "(type LIKE ? OR description LIKE ?) ORDER BY created_at DESC"
    )
    ALL = "SELECT * FROM transactions ORDER BY created_at DESC LIMIT 500"


class OtpQ:
    INSERT = (
        "INSERT INTO otp_codes(subject, code_hash, expires_at) VALUES(?,?, ?)"
    )
    LATEST = (
        "SELECT * FROM otp_codes WHERE subject = ? AND consumed = 0 "
        "ORDER BY id DESC LIMIT 1"
    )
    CONSUME = "UPDATE otp_codes SET consumed = 1 WHERE id = ?"
