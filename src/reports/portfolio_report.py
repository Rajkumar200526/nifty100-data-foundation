import pandas as pd
from pathlib import Path
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

BASE_DIR = Path(__file__).resolve().parents[2]

ranking = pd.read_excel(BASE_DIR / "output" / "company_ranking.xlsx")

companies = pd.read_excel(
    BASE_DIR / "data" / "raw" / "companies.xlsx"
)

df = ranking.merge(
    companies[["company_id", "ticker", "broad_sector"]],
    on="company_id",
    how="left"
)

styles = getSampleStyleSheet()

output_folder = BASE_DIR / "reports" / "portfolio"
output_folder.mkdir(parents=True, exist_ok=True)

pdf = output_folder / "Portfolio_Report.pdf"

doc = SimpleDocTemplate(str(pdf))

elements = []

elements.append(
    Paragraph(
        "<b>N100 Financial Intelligence Platform</b>",
        styles["Title"]
    )
)

elements.append(
    Paragraph(
        "Executive Portfolio Report",
        styles["Heading1"]
    )
)

elements.append(Spacer(1, 12))

summary = [
    ["Metric", "Value"],
    ["Total Companies", str(len(df))],
    ["Average Score", f"{df['overall_score'].mean():.2f}"],
    ["Highest Score", f"{df['overall_score'].max():.2f}"],
    ["Lowest Score", f"{df['overall_score'].min():.2f}"],
]

summary_table = Table(summary, colWidths=[220, 180])

summary_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.navy),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
]))

elements.append(summary_table)

elements.append(Spacer(1, 20))

elements.append(
    Paragraph(
        "<b>Top Ranked Companies</b>",
        styles["Heading2"]
    )
)

top10 = df.sort_values("rank").head(10)

table_data = [["Rank", "Company", "Sector", "Score"]]

for _, row in top10.iterrows():
    table_data.append([
        int(row["rank"]),
        row["company_name"],
        row["broad_sector"],
        f"{row['overall_score']:.2f}"
    ])

table = Table(table_data, colWidths=[50, 170, 150, 70])

table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
]))

elements.append(table)

doc.build(elements)

print("Portfolio report generated successfully.")