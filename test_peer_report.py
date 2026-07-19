import sqlite3
import pandas as pd

from src.analytics.peer import calculate_peer_percentiles
from src.analytics.peer_report import export_peer_report

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

export_peer_report(
    df,
    "output/peer_comparison.xlsx"
)