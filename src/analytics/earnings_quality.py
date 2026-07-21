import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

profit_df = pd.read_sql("""
SELECT
    company_id,
    year,
    sales,
    operating_profit,
    net_profit,
    other_income,
    interest,
    eps
FROM profitandloss;
""", conn)

print(profit_df.head())
# Profit Margin
profit_df["profit_margin"] = (
    profit_df["net_profit"] / profit_df["sales"]
)

profit_margin = (
    profit_df
    .groupby("company_id")["profit_margin"]
    .mean()
    .reset_index()
)

print("\nProfit Margin")
print(profit_margin)
# Operating Margin
profit_df["operating_margin"] = (
    profit_df["operating_profit"] / profit_df["sales"]
)

operating_margin = (
    profit_df
    .groupby("company_id")["operating_margin"]
    .mean()
    .reset_index()
)

print("\nOperating Margin")
print(operating_margin)
# EPS Growth
eps_growth = (
    profit_df
    .groupby("company_id")["eps"]
    .agg(["first", "last"])
    .reset_index()
)

eps_growth["eps_growth"] = (
    (eps_growth["last"] - eps_growth["first"]) /
    eps_growth["first"]
)

print("\nEPS Growth")
print(eps_growth)
earnings_quality = (
    profit_margin
    .merge(operating_margin, on="company_id")
    .merge(
        eps_growth[["company_id", "eps_growth"]],
        on="company_id"
    )
)

print("\nEarnings Quality")
print(earnings_quality)
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

earnings_quality.to_excel(
    output_dir / "earnings_quality.xlsx",
    index=False
)

print("\n✅ earnings_quality.xlsx saved successfully!")

conn.close()

conn.close()