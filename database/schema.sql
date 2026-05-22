-- NovaBank — schema
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name       TEXT    NOT NULL,
    dob             TEXT    NOT NULL,
    mobile          TEXT    NOT NULL,
    address         TEXT    NOT NULL,
    username        TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    pin_hash        TEXT    NOT NULL,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_customers_username ON customers(username);

CREATE TABLE IF NOT EXISTS accounts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number  TEXT    NOT NULL UNIQUE,
    customer_id     INTEGER NOT NULL,
    balance         REAL    NOT NULL DEFAULT 0,
    status          TEXT    NOT NULL DEFAULT 'ACTIVE'  CHECK(status IN ('ACTIVE','FROZEN','CLOSED')),
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_accounts_acctno ON accounts(account_number);
CREATE INDEX IF NOT EXISTS idx_accounts_customer ON accounts(customer_id);

CREATE TABLE IF NOT EXISTS admins (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    role            TEXT    NOT NULL DEFAULT 'ADMIN',
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS transactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id      INTEGER NOT NULL,
    type            TEXT    NOT NULL CHECK(type IN ('DEPOSIT','WITHDRAW','TRANSFER_IN','TRANSFER_OUT')),
    amount          REAL    NOT NULL CHECK(amount > 0),
    balance_after   REAL    NOT NULL,
    description     TEXT,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_tx_account ON transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_tx_date ON transactions(created_at);

CREATE TABLE IF NOT EXISTS otp_codes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    subject     TEXT    NOT NULL,
    code_hash   TEXT    NOT NULL,
    expires_at  TEXT    NOT NULL,
    consumed    INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_otp_subject ON otp_codes(subject);
