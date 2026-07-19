import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql_query("""
SELECT *
FROM profitandloss
ORDER BY company_id, year;
""", conn)

print(df)

conn.close()