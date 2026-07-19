import sqlite3
import pandas as pd
import numpy as np

from src.analytics.radar import create_radar

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

company = df.iloc[0]

labels = [
    "ROE",
    "ROCE",
    "NPM",
    "ROA",
    "Asset Turnover"
]

for _, company in df.iterrows():

    values = np.array([
        company["roe"],
        company["roce"],
        company["net_profit_margin_pct"],
        company["roa"],
        company["asset_turnover"]
    ])

    output = (
        "reports/radar_charts/"
        + company["company_name"]
        + "_radar.png"
    )

    create_radar(
        company["company_name"],
        values,
        labels,
        output
    )

print("All Radar Charts Generated")