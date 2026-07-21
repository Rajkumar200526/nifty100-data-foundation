import pandas as pd
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

BASE_DIR = Path(__file__).resolve().parents[2]

ranking = pd.read_excel(BASE_DIR / "output" / "company_ranking.xlsx")
companies = pd.read_excel(BASE_DIR / "data" / "raw" / "companies.xlsx")

# Merge ranking with company details
df = ranking.merge(
    companies[["company_id", "ticker", "broad_sector"]],
    on="company_id",
    how="left"
)

styles = getSampleStyleSheet()

output_folder = BASE_DIR / "reports" / "sector"
output_folder.mkdir(parents=True, exist_ok=True)

for sector in sorted(df["broad_sector"].dropna().unique()):

    sector_df = df[df["broad_sector"] == sector].sort_values("rank")

    pdf_path = output_folder / f"{sector.replace(' ', '_')}_Report.pdf"

    doc = SimpleDocTemplate(str(pdf_path))

    elements = []

    elements.append(
        Paragraph(
            f"<b>{sector} Sector Report</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            f"Companies in Sector: {len(sector_df)}",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Average Score: {sector_df['overall_score'].mean():.2f}",
            styles["Heading2"]
        )
    )

    top_company = sector_df.iloc[0]

    elements.append(
        Paragraph(
            f"Top Performer: {top_company['company_name']} ({top_company['overall_score']:.2f})",
            styles["Heading2"]
        )
    )

    table_data = [["Rank", "Company", "Ticker", "Score"]]

    for _, row in sector_df.iterrows():
        table_data.append([
            int(row["rank"]),
            row["company_name"],
            row["ticker"],
            f"{row['overall_score']:.2f}"
        ])

    table = Table(table_data, colWidths=[60, 170, 90, 80])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.navy),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    elements.append(table)

    doc.build(elements)

print("Sector reports generated successfully.")