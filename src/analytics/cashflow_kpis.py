import sqlite3
import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"
conn = sqlite3.connect(DB_PATH)
cashflow_df = pd.read_sql("""
SELECT
    company_id,
    year,
    operating_cashflow,
    investing_cashflow,
    financing_cashflow
FROM cashflow;
""", conn)

profit_df = pd.read_sql("""
SELECT
    company_id,
    year,
    net_profit
FROM profitandloss;
""", conn)

cashflow_df = cashflow_df.merge(
    profit_df,
    on=["company_id", "year"],
    how="left"
)

# ===========================
# ADD THE NEW CODE HERE
# ===========================

# Calculate CFO/PAT Ratio
cashflow_df["cfo_pat_ratio"] = (
    cashflow_df["operating_cashflow"] /
    cashflow_df["net_profit"]
)

# Average CFO/PAT Ratio over 5 years
cfo_quality = (
    cashflow_df
    .groupby("company_id")["cfo_pat_ratio"]
    .mean()
    .reset_index()
)

# Classify CFO Quality
def classify_cfo_quality(ratio):
    if ratio > 1.0:
        return "High Quality"
    elif ratio >= 0.5:
        return "Moderate"
    else:
        return "Accrual Risk"

cfo_quality["cfo_quality_label"] = (
    cfo_quality["cfo_pat_ratio"]
    .apply(classify_cfo_quality)
)

print(cfo_quality)
# Calculate CapEx Intensity
cashflow_df["capex_intensity"] = (
    cashflow_df["investing_cashflow"].abs() /
    cashflow_df["operating_cashflow"].abs()
)

capex = (
    cashflow_df
    .groupby("company_id")["capex_intensity"]
    .mean()
    .reset_index()
)

print("\nCapEx Intensity")
print(capex)
# Distress Signal
cashflow_df["distress_signal"] = (
    (cashflow_df["operating_cashflow"] < 0) &
    (cashflow_df["financing_cashflow"] > 0)
)

distress = (
    cashflow_df
    .groupby("company_id")["distress_signal"]
    .sum()
    .reset_index()
)

print("\nDistress Signal")
print(distress)
# Deleveraging Flag
cashflow_df["deleveraging_flag"] = (
    cashflow_df["financing_cashflow"] < 0
)

deleveraging = (
    cashflow_df
    .groupby("company_id")["deleveraging_flag"]
    .sum()
    .reset_index()
)

print("\nDeleveraging Flag")
print(deleveraging)
cashflow_intelligence = (
    cfo_quality
    .merge(capex, on="company_id")
    .merge(distress, on="company_id")
    .merge(deleveraging, on="company_id")
)

print("\nCash Flow Intelligence")
print(cashflow_intelligence)
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

cashflow_intelligence.to_excel(
    output_dir / "cashflow_intelligence.xlsx",
    index=False
)

print("\n✅ cashflow_intelligence.xlsx saved successfully!")
# ===========================
# END OF NEW CODE
# ===========================

conn.close()