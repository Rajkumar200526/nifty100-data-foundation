import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ranking = pd.read_excel(BASE_DIR / "output" / "company_ranking.xlsx")

records = []

for _, row in ranking.iterrows():

    pros = []
    cons = []

    if row["profit_margin"] >= 20:
        pros.append("Strong profit margin")

    if row["operating_margin"] >= 15:
        pros.append("Healthy operating margin")

    if row["eps_growth"] > 0:
        pros.append("Positive EPS growth")

    if row["debt_equity"] <= 0.5:
        pros.append("Low debt burden")
    else:
        cons.append("High debt-equity ratio")

    if row["distress_signal"] == "Yes":
        cons.append("Financial distress detected")

    if row["cfo_quality_label"] == "High Quality":
        pros.append("High-quality operating cash flow")

    records.append({
        "company_id": row["company_id"],
        "company_name": row["company_name"],
        "pros": "; ".join(pros),
        "cons": "; ".join(cons)
    })

output = pd.DataFrame(records)

output.to_csv(
    BASE_DIR / "output" / "pros_cons_generated.csv",
    index=False
)

print("Pros & Cons generated successfully.")