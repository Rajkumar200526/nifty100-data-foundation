import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

balance_df = pd.read_sql("""
SELECT *
FROM balancesheet;
""", conn)

print(balance_df.head())
# Net Worth
balance_df["net_worth"] = (
    balance_df["equity_capital"] +
    balance_df["reserves"]
)

print(balance_df[
    [
        "company_id",
        "year",
        "net_worth"
    ]
].head())
# Debt-to-Equity Ratio
balance_df["debt_equity"] = (
    balance_df["borrowings"] /
    balance_df["net_worth"]
)

de_ratio = (
    balance_df
    .groupby("company_id")["debt_equity"]
    .mean()
    .reset_index()
)

print("\nDebt to Equity")
print(de_ratio)
# Asset Utilization
balance_df["asset_utilization"] = (
    balance_df["investments"] /
    balance_df["total_assets"]
)

asset_util = (
    balance_df
    .groupby("company_id")["asset_utilization"]
    .mean()
    .reset_index()
)

print("\nAsset Utilization")
print(asset_util)
financial_health = (
    de_ratio
    .merge(asset_util, on="company_id")
)

print("\nFinancial Health")
print(financial_health)
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

financial_health.to_excel(
    output_dir / "financial_health.xlsx",
    index=False
)

print("\n✅ financial_health.xlsx saved successfully!")

conn.close()

conn.close()