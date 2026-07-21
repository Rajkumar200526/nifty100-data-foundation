import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

df = pd.read_excel(BASE_DIR / "output" / "company_ranking.xlsx")

recommendations = []

for _, row in df.iterrows():

    score = row["overall_score"]

    if score >= 85:
        recommendation = "Strong Buy"
    elif score >= 70:
        recommendation = "Buy"
    elif score >= 55:
        recommendation = "Hold"
    elif score >= 40:
        recommendation = "Reduce"
    else:
        recommendation = "Sell"

    recommendations.append({
        "company_id": row["company_id"],
        "company_name": row["company_name"],
        "overall_score": round(score, 2),
        "recommendation": recommendation
    })

output = pd.DataFrame(recommendations)

output.to_excel(
    BASE_DIR / "output" / "investment_recommendations.xlsx",
    index=False
)

print("Investment recommendations generated successfully.")