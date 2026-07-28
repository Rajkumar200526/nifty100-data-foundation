import sqlite3

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

tables = [
    "companies",
    "financial_ratios",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "stock_prices",
    "sectors",
    "company_clusters"
]

print("\n========== ROW COUNTS ==========\n")

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:<20} : {count}")

conn.close()