import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(company_clusters);")

print("Columns in company_clusters:\n")

for column in cursor.fetchall():
    print(column)

conn.close()