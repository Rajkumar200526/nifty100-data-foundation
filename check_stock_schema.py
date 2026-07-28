import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(stock_prices);")

columns = cursor.fetchall()

print("Columns in stock_prices:\n")

for column in columns:
    print(column)

conn.close()