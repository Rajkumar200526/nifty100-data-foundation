import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(profitandloss);")

columns = cursor.fetchall()

for column in columns:
    print(column)

conn.close()