import pandas as pd
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[2]
conn = sqlite3.connect(BASE_DIR / "db" / "nifty100.db")

companies = pd.read_sql(
    "SELECT company_id, company_name FROM companies",
    conn
)

cashflow = pd.read_excel(
    BASE_DIR / "output" / "cashflow_intelligence.xlsx"
)

earnings = pd.read_excel(
    BASE_DIR / "output" / "earnings_quality.xlsx"
)

financial = pd.read_excel(
    BASE_DIR / "output" / "financial_health.xlsx"
)
ranking = (
    cashflow
    .merge(earnings, on="company_id")
    .merge(financial, on="company_id")
    .merge(companies, on="company_id", how="left")
)

print(ranking.head())
print("\nColumns in ranking:")
print(ranking.columns.tolist())
# Initialize Composite Score
ranking["overall_score"] = 0
ranking["overall_score"] += (
    ranking["cfo_pat_ratio"] * 30
)
# Add Profit Margin Score (25%)
ranking["overall_score"] += (
    ranking["profit_margin"] * 25
)
# Add Operating Margin Score (20%)
ranking["overall_score"] += (
    ranking["operating_margin"] * 20
)
# Add Debt-to-Equity Score (15%)
ranking["overall_score"] += (
    (1 - ranking["debt_equity"]) * 15
)
# Add Asset Utilization Score (10%)
ranking["overall_score"] += (
    (1 - ranking["asset_utilization"]) * 10
)
print("\nFinal Composite Score")
print(
    ranking[
        [
            "company_id",
            "overall_score"
        ]
    ]
)
# Generate Rank
ranking["rank"] = (
    ranking["overall_score"]
    .rank(
        ascending=False,
        method="dense"
    )
    .astype(int)
)
ranking = ranking.sort_values("rank")
print("\n==============================")
print(" NIFTY 100 COMPANY RANKING")
print("==============================")

print(
    ranking[
        [
            "rank",
            "company_id",
            "overall_score",
            "cfo_quality_label"
        ]
    ]
)
output_dir = BASE_DIR / "output"
output_dir.mkdir(exist_ok=True)

ranking.to_excel(
    output_dir / "company_ranking.xlsx",
    index=False
)
print("\n✅ company_ranking.xlsx saved successfully!")