from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT = BASE_DIR / "output"

scores_file = OUTPUT / "company_scores.csv"

df = pd.read_csv(scores_file)

# ----------------------------------------------------
# Select Top Companies
# ----------------------------------------------------

TOP_N = 5

portfolio = df.sort_values(
    "Investment Score",
    ascending=False
).head(TOP_N).copy()

# ----------------------------------------------------
# Equal Allocation
# ----------------------------------------------------

portfolio["Allocation (%)"] = round(100 / TOP_N, 2)

# ----------------------------------------------------
# Portfolio Summary
# ----------------------------------------------------

summary = {
    "Total Companies": len(portfolio),
    "Average Investment Score": round(
        portfolio["Investment Score"].mean(), 2
    ),
    "Highest Score": round(
        portfolio["Investment Score"].max(), 2
    ),
    "Lowest Score": round(
        portfolio["Investment Score"].min(), 2
    )
}

# ----------------------------------------------------
# Save Portfolio
# ----------------------------------------------------

portfolio.to_csv(
    OUTPUT / "recommended_portfolio.csv",
    index=False
)

summary_df = pd.DataFrame([summary])

summary_df.to_csv(
    OUTPUT / "portfolio_summary.csv",
    index=False
)

print("\nRecommended Portfolio\n")
print(portfolio)

print("\nPortfolio Summary\n")
print(summary_df)

print("\n✓ recommended_portfolio.csv created")
print("✓ portfolio_summary.csv created")