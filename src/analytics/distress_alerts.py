import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ranking = pd.read_excel(BASE_DIR / "output" / "company_ranking.xlsx")

alerts = ranking[
    (ranking["distress_signal"] == "Yes") |
    (ranking["debt_equity"] > 2) |
    (ranking["profit_margin"] < 5)
].copy()

alerts = alerts.sort_values("overall_score")

output = BASE_DIR / "output" / "distress_alerts.csv"

alerts.to_csv(output, index=False)

print(f"{len(alerts)} distress alerts generated.")