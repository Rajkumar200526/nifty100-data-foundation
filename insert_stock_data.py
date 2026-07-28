import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

data = [
    (1, "2026-07-20", 3595),
    (1, "2026-07-21", 3608),
    (1, "2026-07-22", 3635),
    (1, "2026-07-23", 3652),
    (1, "2026-07-24", 3670),

    (2, "2026-07-20", 1592),
    (2, "2026-07-21", 1598),
    (2, "2026-07-22", 1608),
    (2, "2026-07-23", 1616),
    (2, "2026-07-24", 1625),
]

cursor.executemany("""
INSERT INTO stock_prices
(company_id, trade_date, close_price)
VALUES (?, ?, ?)
""", data)

conn.commit()
conn.close()

print("Stock prices inserted successfully.")