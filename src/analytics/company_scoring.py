import sqlite3
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"
OUTPUT = BASE_DIR / "output"

OUTPUT.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    fr.company_id,
    fr.company_name,
    c.broad_sector,
    fr.year,
    fr.sales,
    fr.operating_profit,
    fr.net_profit,
    fr.roe,
    fr.roce,
    fr.debt_to_equity,
    fr.free_cash_flow
FROM financial_ratios fr
JOIN companies c
ON fr.company_id = c.company_id
WHERE fr.year = (
    SELECT MAX(year)
    FROM financial_ratios
)
"""

df = pd.read_sql(query, conn)
conn.close()

# -----------------------------
# Normalize Metrics
# -----------------------------

positive_metrics = [
    "sales",
    "operating_profit",
    "net_profit",
    "roe",
    "roce",
    "free_cash_flow"
]

negative_metrics = [
    "debt_to_equity"
]

scaler = MinMaxScaler()

df[positive_metrics] = scaler.fit_transform(df[positive_metrics])
df[negative_metrics] = 1 - scaler.fit_transform(df[negative_metrics])

# -----------------------------
# Scores
# -----------------------------

df["Growth Score"] = (
    df["sales"] * 0.40 +
    df["operating_profit"] * 0.30 +
    df["free_cash_flow"] * 0.30
) * 100

df["Profitability Score"] = (
    df["roe"] * 0.50 +
    df["roce"] * 0.50
) * 100

df["Risk Score"] = (
    df["debt_to_equity"]
) * 100

df["Investment Score"] = (
    df["Growth Score"] * 0.40 +
    df["Profitability Score"] * 0.40 +
    df["Risk Score"] * 0.20
)

# -----------------------------
# Ranking
# -----------------------------

df["Rank"] = (
    df["Investment Score"]
    .rank(ascending=False, method="dense")
    .astype(int)
)

# -----------------------------
# Recommendation
# -----------------------------

def recommendation(score):
    if score >= 80:
        return "Strong Buy"
    elif score >= 65:
        return "Buy"
    elif score >= 50:
        return "Hold"
    elif score >= 35:
        return "Reduce"
    else:
        return "Sell"

df["Recommendation"] = df["Investment Score"].apply(recommendation)

# -----------------------------
# Save Results
# -----------------------------

result = df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "Investment Score",
        "Rank",
        "Recommendation"
    ]
].sort_values("Rank")

result.to_csv(
    OUTPUT / "company_scores.csv",
    index=False
)

print(result)

print("\n✓ company_scores.csv created successfully.")