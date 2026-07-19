"""
Sprint 3 - Day 15
Financial Screener Engine
"""
from src.analytics.composite_score import calculate_score
import sqlite3
import pandas as pd
import yaml
with open("config/screener_config.yaml", "r") as file:
    config = yaml.safe_load(file)

conn = sqlite3.connect("db/nifty100.db")
df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)
def apply_filters(df, config):
    """
    Apply screener filters from YAML configuration.
    """

    filtered_df = df.copy()

    # ROE Filter
    if "roe_min" in config:
        filtered_df = filtered_df[
            filtered_df["roe"] >= config["roe_min"]
        ]

    # Debt-to-Equity Filter
    if "debt_to_equity_max" in config:
        filtered_df = filtered_df[
            filtered_df["debt_to_equity"] <= config["debt_to_equity_max"]
        ]
        # Free Cash Flow Filter
    if "free_cash_flow_min" in config:
        filtered_df = filtered_df[
            filtered_df["free_cash_flow"] >= config["free_cash_flow_min"]
    ]
        # Sales Filter
    if "sales_min" in config:
        filtered_df = filtered_df[
            filtered_df["sales"] >= config["sales_min"]
    ]
        # Operating Profit Margin Filter
    #if "opm_min" in config:
    #   filtered_df = filtered_df[
    #      filtered_df["operating_profit_margin_pct"] >= config["opm_min"]
    #]
    # Asset Turnover Filter
    if "asset_turnover_min" in config:
        filtered_df = filtered_df[
            filtered_df["asset_turnover"] >= config["asset_turnover_min"]
    ]
# Interest Coverage Filter
    if "interest_coverage_min" in config:
       filtered_df = filtered_df[
            filtered_df["interest_coverage"] >= config["interest_coverage_min"]
    ]
       filtered_df["composite_quality_score"] = calculate_score(filtered_df)
    filtered_df["composite_quality_score"] = calculate_score(filtered_df)
    print(filtered_df.columns)
    filtered_df = filtered_df.sort_values(
    by="composite_quality_score",
    ascending=False
    )
    return filtered_df

if __name__ == "__main__":

    conn = sqlite3.connect("db/nifty100.db")

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    filtered_df = apply_filters(df, config)

    print("\n=== Screening Results ===\n")

    print(
        filtered_df[
            [
                "company_name",
                "roe",
                "debt_to_equity",
                "asset_turnover",
                "interest_coverage",
                "free_cash_flow",
                "sales"
            ]
        ]
    )

    print(f"\nCompanies Selected: {len(filtered_df)}")