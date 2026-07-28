import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

REPORTS = BASE_DIR / "reports"
OUTPUT = BASE_DIR / "output"

REPORTS.mkdir(exist_ok=True)
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

cluster_file = OUTPUT / "cluster_labels.csv"

clusters = pd.read_csv(cluster_file)

df = df.merge(
    clusters[
        [
            "company_id",
            "cluster_id",
            "cluster_name"
        ]
    ],
    on="company_id"
)
# ----------------------------------------------------
# Cluster Profile
# ----------------------------------------------------

profile = (
    df.groupby(["cluster_id", "cluster_name"])[
        [
            "sales",
            "operating_profit",
            "net_profit",
            "roe",
            "roce",
            "debt_to_equity",
            "free_cash_flow",
        ]
    ]
    .agg(["mean", "median"])
)

profile.to_csv(OUTPUT / "cluster_profile.csv")

print("✓ cluster_profile.csv created")
# ----------------------------------------------------
# Portfolio Statistics
# ----------------------------------------------------

metrics = [
    "sales",
    "operating_profit",
    "net_profit",
    "roe",
    "roce",
    "debt_to_equity",
    "free_cash_flow",
]

stats = pd.DataFrame(index=metrics)

stats["P10"] = df[metrics].quantile(0.10)
stats["P25"] = df[metrics].quantile(0.25)
stats["P50"] = df[metrics].quantile(0.50)
stats["P75"] = df[metrics].quantile(0.75)
stats["P90"] = df[metrics].quantile(0.90)
stats["Mean"] = df[metrics].mean()
stats["Std"] = df[metrics].std()

stats.to_csv(OUTPUT / "portfolio_stats.csv")

print("✓ portfolio_stats.csv created")
# ----------------------------------------------------
# Correlation Heatmap
# ----------------------------------------------------

corr = df[metrics].corr()

plt.figure(figsize=(10, 8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Financial KPI Correlation Matrix")

plt.tight_layout()

plt.savefig(REPORTS / "correlation_heatmap.png")

plt.close()

print("✓ correlation_heatmap.png created")
# ----------------------------------------------------
# Outlier Detection
# ----------------------------------------------------

outliers = []

for sector, group in df.groupby("broad_sector"):

    temp = group.copy()

    for metric in metrics:

        temp[f"{metric}_z"] = zscore(temp[metric], nan_policy="omit")

    mask = (
        temp[[f"{m}_z" for m in metrics]]
        .abs()
        .gt(3)
        .any(axis=1)
    )

    outliers.append(temp.loc[mask])

outlier_df = pd.concat(outliers, ignore_index=True)

outlier_df.to_csv(
    OUTPUT / "outlier_report.csv",
    index=False
)

print("✓ outlier_report.csv created")

print("\nDay 37 completed successfully.")