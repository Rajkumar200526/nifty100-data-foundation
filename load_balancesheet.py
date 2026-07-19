import pandas as pd
import sqlite3

# Read the Excel file
df = pd.read_excel("data/raw/balancesheet.xlsx")

# Connect to the database
conn = sqlite3.connect("db/nifty100.db")

# Load data into the balancesheet table
df.to_sql(
    "balancesheet",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Balance Sheet data loaded successfully!")