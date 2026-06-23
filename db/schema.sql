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