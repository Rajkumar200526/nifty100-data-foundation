import sqlite3
import pandas as pd

df = pd.read_excel("data/raw/cashflow.xlsx")

df = df.rename(columns={
    "operating_activity": "operating_cashflow",
    "investing_activity": "investing_cashflow",
    "financing_activity": "financing_cashflow"
})

conn = sqlite3.connect("db/nifty100.db")

conn.execute("DELETE FROM cashflow")

df.to_sql("cashflow", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print(f"Inserted {len(df)} rows into cashflow table.")