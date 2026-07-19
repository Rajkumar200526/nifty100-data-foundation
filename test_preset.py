import sqlite3
import pandas as pd

from src.screener.presets import quality_compounder
from src.screener.presets import value_pick
from src.screener.presets import (
    quality_compounder,
    value_pick,
    growth_accelerator,
)

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

result = quality_compounder(df)

print("\n=== Quality Compounder ===\n")

print(
    result[
        [
            "company_name",
            "roe",
            "debt_to_equity",
            "free_cash_flow",
            "composite_quality_score",
        ]
    ]
)

print(f"\nCompanies Selected: {len(result)}")
print("\n=== Value Pick ===\n")

value_result = value_pick(df)

print(
    value_result[
        [
            "company_name",
            "debt_to_equity"
        ]
    ]
)

print(f"\nCompanies Selected: {len(value_result)}")
from src.screener.presets import growth_accelerator

print("\n=== Growth Accelerator ===\n")

growth_result = growth_accelerator(df)

print(
    growth_result[
        [
            "company_name",
            "debt_to_equity"
        ]
    ]
)

print(f"\nCompanies Selected: {len(growth_result)}")
with pd.ExcelWriter("output/screener_output.xlsx") as writer:

    quality_compounder(df).to_excel(
        writer,
        sheet_name="Quality Compounder",
        index=False
    )

    value_pick(df).to_excel(
        writer,
        sheet_name="Value Pick",
        index=False
    )

    growth_accelerator(df).to_excel(
        writer,
        sheet_name="Growth Accelerator",
        index=False
    )

print("Excel Report Generated Successfully")