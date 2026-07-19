import pandas as pd
import sqlite3

# Read Excel file
df = pd.read_excel("data/raw/companies.xlsx")

# Keep all columns from the Excel file
df = pd.read_excel("data/raw/companies.xlsx")

# Connect to the database
conn = sqlite3.connect("db/nifty100.db")

# Replace existing data
df.to_sql(
    "companies",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Companies loaded successfully!")