import sqlite3

DATABASE = "db/nifty100.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table';
""")

tables = cursor.fetchall()

print("Tables in database:\n")

for table in tables:
    print(table[0])

conn.close()