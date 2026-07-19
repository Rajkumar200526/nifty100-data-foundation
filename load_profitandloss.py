import pandas as pd
import sqlite3

# Read the Excel file
df = pd.read_excel("data/raw/profitandloss.xlsx")

# Connect to the database
conn = sqlite3.connect("db/nifty100.db")

# Load data into the profitandloss table
df.to_sql(
    "profitandloss",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Profit & Loss data loaded successfully!")