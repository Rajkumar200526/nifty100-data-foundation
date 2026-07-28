import sqlite3
import pandas as pd
import numpy as np

from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.stats import zscore


# ----------------------------------------------------
# Paths
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

REPORTS_DIR = BASE_DIR / "reports"
OUTPUT_DIR = BASE_DIR / "output"

REPORTS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    fr.company_id,
    fr.company_name,
    c.broad_sector,
    fr.year,
    fr.roe,
    fr.roce,
    fr.debt_to_equity,
    fr.free_cash_flow,
    fr.operating_profit
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


# ----------------------------------------------------
# Features
# ----------------------------------------------------

features = [
    "roe",
    "roce",
    "debt_to_equity",
    "free_cash_flow",
    "operating_profit",
]


# ----------------------------------------------------
# Fill Missing Values
# ----------------------------------------------------

for feature in features:

    df[feature] = (
        df.groupby("broad_sector")[feature]
        .transform(lambda x: x.fillna(x.median()))
    )


# ----------------------------------------------------
# Standard Scaling
# ----------------------------------------------------

scaler = StandardScaler()

X = scaler.fit_transform(df[features])


# ----------------------------------------------------
# Elbow Plot
# ----------------------------------------------------

inertia = []

for k in range(2, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X)

    inertia.append(model.inertia_)


plt.figure(figsize=(8,5))

plt.plot(
    range(2,11),
    inertia,
    marker="o"
)

plt.title("KMeans Elbow Curve")
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")

plt.grid(True)

plt.savefig(REPORTS_DIR / "elbow_plot.png")

plt.close()
# ----------------------------------------------------
# Correlation Heatmap
# ----------------------------------------------------

correlation = df[features].corr()

plt.figure(figsize=(8, 6))

plt.imshow(correlation, cmap="coolwarm", interpolation="nearest")

plt.colorbar()

plt.xticks(range(len(features)), features, rotation=45)
plt.yticks(range(len(features)), features)

plt.title("Financial Ratio Correlation Heatmap")

for i in range(len(features)):
    for j in range(len(features)):
        plt.text(
            j,
            i,
            f"{correlation.iloc[i, j]:.2f}",
            ha="center",
            va="center",
            fontsize=8
        )

plt.tight_layout()

plt.savefig(REPORTS_DIR / "correlation_heatmap.png")

plt.close()

# ----------------------------------------------------
# Outlier Detection (Z-Score)
# ----------------------------------------------------

z_scores = np.abs(zscore(df[features]))

threshold = 3

outlier_mask = (z_scores > threshold).any(axis=1)

outliers = df.loc[outlier_mask, [
    "company_id",
    "company_name",
    "broad_sector",
    "year"
] + features]

outliers.to_csv(
    OUTPUT_DIR / "outlier_report.csv",
    index=False
)

print(f"\nOutliers Found: {len(outliers)}")
# ----------------------------------------------------
# Portfolio Statistics
# ----------------------------------------------------

portfolio_stats = df[features].describe().T

portfolio_stats["median"] = df[features].median()

portfolio_stats = portfolio_stats[
    [
        "count",
        "mean",
        "median",
        "std",
        "min",
        "25%",
        "50%",
        "75%",
        "max",
    ]
]

portfolio_stats.to_csv(
    OUTPUT_DIR / "portfolio_statistics.csv"
)

print("\nPortfolio Statistics Generated")
# ----------------------------------------------------
# Final Model
# ----------------------------------------------------

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

df["cluster_id"] = kmeans.fit_predict(X)


# ----------------------------------------------------
# Distance From Centroid
# ----------------------------------------------------

distances = kmeans.transform(X)

df["distance_from_centroid"] = distances.min(axis=1)


# ----------------------------------------------------
# Cluster Names
# ----------------------------------------------------

cluster_names = {
    0: "High Quality Compounders",
    1: "Defensive Dividend",
    2: "Emerging Growth",
    3: "Value Cyclicals",
    4: "Turnaround"
}

df["cluster_name"] = df["cluster_id"].map(cluster_names)


# ----------------------------------------------------
# Save CSV
# ----------------------------------------------------

output = df[
    [
        "company_id",
        "company_name",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"
    ]
]

output.to_csv(
    OUTPUT_DIR / "cluster_labels.csv",
    index=False
)

print("\nClustering Complete")

print(output.head())
# ----------------------------------------------------
# Update company_clusters table
# ----------------------------------------------------

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        UPDATE company_clusters
        SET cluster = ?,
            cluster_name = ?
        WHERE company_id = ?
    """, (
        int(row["cluster_id"]),
        row["cluster_name"],
        int(row["company_id"])
    ))

conn.commit()
conn.close()

print("\ncompany_clusters table updated successfully.")