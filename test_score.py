import sqlite3
import pandas as pd

from src.analytics.composite_score import calculate_score

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

df["composite_quality_score"] = calculate_score(df)

df = df.sort_values(
    by="composite_quality_score",
    ascending=False
)

print(
    df[
        [
            "company_name",
            "composite_quality_score"
        ]
    ]
)