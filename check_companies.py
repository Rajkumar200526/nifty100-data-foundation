import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql_query("""
SELECT company_id, company_name
FROM companies
ORDER BY company_name;
""", conn)

print(df)

conn.close()