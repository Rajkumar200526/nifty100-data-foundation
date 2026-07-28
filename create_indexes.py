import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

indexes = [
    """
    CREATE INDEX IF NOT EXISTS idx_company_id
    ON financial_ratios(company_id);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_company_year
    ON financial_ratios(year);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_sector
    ON companies(broad_sector);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_stock_company
    ON stock_prices(company_id);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_stock_date
    ON stock_prices(trade_date);
    """
]

for index in indexes:
    cursor.execute(index)

conn.commit()
conn.close()

print("Database indexes created successfully.")