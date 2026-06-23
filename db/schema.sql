PRAGMA foreign_keys = ON;

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    ticker TEXT UNIQUE
);

CREATE TABLE sectors (
    sector_id INTEGER PRIMARY KEY,
    sector_name TEXT NOT NULL
);

CREATE TABLE financial_ratios (
    ratio_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    roe REAL,
    roce REAL,
    pe_ratio REAL,
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);
CREATE TABLE profitandloss (
    pnl_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    revenue REAL,
    net_profit REAL,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE balancesheet (
    bs_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE cashflow (
    cf_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    operating_cashflow REAL,
    investing_cashflow REAL,
    financing_cashflow REAL,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE stock_prices (
    price_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    trade_date TEXT,
    close_price REAL,
    FOREIGN KEY(company_id)
        REFERENCES companies(company_id)
);