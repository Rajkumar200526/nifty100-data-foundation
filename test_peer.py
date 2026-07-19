import sqlite3
import pandas as pd

from src.analytics.peer import calculate_peer_percentiles

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

df = calculate_peer_percentiles(
    df,
    "roe"
)

print(
    df[
        [
            "company_name",
            "roe",
            "roe_percentile"
        ]
    ]
)