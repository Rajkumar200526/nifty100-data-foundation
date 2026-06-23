import sqlite3
import os

DB_FILE = "db/nifty100.db"

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)

with open("db/schema.sql", "r") as f:
    schema = f.read()

conn.executescript(schema)

conn.commit()
conn.close()

print("Database Created Successfully")