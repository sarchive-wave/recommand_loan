CREATE TABLE IF NOT EXISTS loan_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    rate_display TEXT NOT NULL,
    rate_min REAL NOT NULL,
    limit_display TEXT NOT NULL,
    max_amount INTEGER NOT NULL,
    url TEXT NOT NULL,
    jobs TEXT NOT NULL,
    credits TEXT NOT NULL,
    purposes TEXT NOT NULL,
    collaterals TEXT NOT NULL,
    regions TEXT NOT NULL,
    tags TEXT NOT NULL,
    available INTEGER NOT NULL DEFAULT 1
);
