import sqlite3
import pandas as pd
from src.analytics.ratios import return_on_equity
from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity,
    fcf_conversion_rate,
)

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity,
    fcf_conversion_rate,
)

from src.analytics.cagr import calculate_cagr
DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)
df = pd.read_csv("data/processed/financial_data.csv")
print(df.head())
from src.analytics.ratios import net_profit_margin

df["net_profit_margin_pct"] = df.apply(
    lambda row: net_profit_margin(
        row["net_profit"],
        row["sales"]
    ),
    axis=1
)
df["roe"] = df.apply(
    lambda row: return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

from src.analytics.ratios import return_on_capital_employed
df["roce"] = df.apply(
    lambda row: return_on_capital_employed(
        row["operating_profit"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),
    axis=1
)
df["roa"] = df.apply(
    lambda row: return_on_assets(
        row["net_profit"],
        row["total_assets"]
    ),
    axis=1
)
from src.analytics.ratios import debt_to_equity
df["debt_to_equity"] = df.apply(
    lambda row: debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)
from src.analytics.ratios import interest_coverage_ratio
df["interest_coverage"] = df.apply(
    lambda row: interest_coverage_ratio(
        row["operating_profit"],
        row["other_income"],
        row["interest"]
    ),
    axis=1
)
from src.analytics.ratios import asset_turnover
df["asset_turnover"] = df.apply(
    lambda row: asset_turnover(
        row["sales"],
        row["total_assets"]
    ),
    axis=1
)
df["free_cash_flow"] = df.apply(
    lambda row: free_cash_flow(
        row["operating_activity"],
        row["investing_activity"]
    ),
    axis=1
)
df["capex_pct"] = df.apply(
    lambda row: capex_intensity(
        row["investing_activity"],
        row["sales"]
    )[0],
    axis=1
)

df["capex_label"] = df.apply(
    lambda row: capex_intensity(
        row["investing_activity"],
        row["sales"]
    )[1],
    axis=1
)
df["fcf_conversion"] = df.apply(
    lambda row: fcf_conversion_rate(
        row["free_cash_flow"],
        row["operating_profit"]
    ),
    axis=1
)
print(
    df[
        [
            "company_name",
            "net_profit_margin_pct",
            "roe",
            "roce",
            "roa",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow",
            "capex_pct",
            "capex_label",
            "fcf_conversion",
        ]
    ]
)
import sqlite3

conn = sqlite3.connect("db/nifty100.db")

df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Financial Ratios Loaded Successfully")