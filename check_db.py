import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

print("===== TABLES =====")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

print("\n===== COMPANIES COLUMNS =====")
cursor.execute("PRAGMA table_info(companies)")
for row in cursor.fetchall():
    print(row)

conn.close()