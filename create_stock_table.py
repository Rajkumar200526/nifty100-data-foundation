import sqlite3

DATABASE = "db/nifty100.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    trade_date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);
""")

conn.commit()
conn.close()

print("✅ stock_prices table created successfully.")