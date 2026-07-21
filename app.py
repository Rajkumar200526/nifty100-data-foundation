from flask import Flask, render_template, send_from_directory
import pandas as pd
from pathlib import Path


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

# Load files
ranking = pd.read_excel(BASE_DIR / "output" / "company_ranking.xlsx")
financial_health = pd.read_excel(BASE_DIR / "output" / "financial_health.xlsx")
earnings_quality = pd.read_excel(BASE_DIR / "output" / "earnings_quality.xlsx")
earnings_quality = earnings_quality.merge(
    ranking[["company_id", "company_name"]],
    on="company_id",
    how="left"
)
cashflow = pd.read_excel(BASE_DIR / "output" / "cashflow_intelligence.xlsx")
recommendations = pd.read_excel(BASE_DIR / "output" / "investment_recommendations.xlsx")
distress = pd.read_csv(BASE_DIR / "output" / "distress_alerts.csv")

# Add company names to financial_health
financial_health = financial_health.merge(
    ranking[["company_id", "company_name"]],
    on="company_id",
    how="left"
)

#sector_data = (
 #   ranking.groupby("sector")["overall_score"]
 #   .mean()
 #   .reset_index()
#)

#sector_names = sector_data["sector"].tolist()
#sector_scores = sector_data["overall_score"].round(2).tolist()

total_companies = len(ranking)
top_score = ranking["overall_score"].max()
average_score = ranking["overall_score"].mean()

company_names = ranking["company_name"].tolist()

company_scores = ranking["overall_score"].tolist()
top5 = ranking.nlargest(5, "overall_score")

@app.route("/")
def home():
    return render_template(
        "index.html",
        companies=ranking.to_dict(orient="records"),
        total_companies=total_companies,
        top_score=round(top_score, 2),
        average_score=round(average_score, 2),
        company_names=company_names,
        company_scores=company_scores,
        top5=top5.to_dict(orient="records"),
    )
@app.route("/company/<int:company_id>")
def company_details(company_id):
    company = ranking[ranking["company_id"] == company_id]

    if company.empty:
        return "Company not found", 404

    company = company.iloc[0]

    return render_template(
        "company.html",
        company=company
    )
@app.route("/recommendations")
def recommendation_page():
    return render_template(
        "recommendations.html",
        data=recommendations.to_dict(orient="records")
    )


@app.route("/distress")
def distress_page():
    return render_template(
        "distress.html",
        data=distress.to_dict(orient="records")
    )


@app.route("/financial-health")
def financial_page():
    return render_template(
        "financial_health.html",
        data=financial_health.to_dict(orient="records")
    )
cashflow = cashflow.merge(
    ranking[["company_id", "company_name"]],
    on="company_id",
    how="left"
)


@app.route("/cashflow")
def cashflow_page():
    return render_template(
        "cashflow.html",
        data=cashflow.to_dict(orient="records")
    )


@app.route("/earnings")
def earnings_page():
    return render_template(
        "earnings.html",
        data=earnings_quality.to_dict(orient="records")
    )
@app.route("/ranking")
def ranking_page():
    return render_template(
        "ranking.html",
        companies=ranking.to_dict(orient="records")
    )
@app.route("/reports")
def reports():
    return render_template("reports.html")
@app.route("/test")
def test():
    return {
        "company_names": company_names,
        "company_scores": company_scores
    }
@app.route("/download/company-ranking")
def download_company_ranking():
    return send_from_directory(
        BASE_DIR / "output",
        "company_ranking.xlsx",
        as_attachment=True
    )


@app.route("/download/financial-health")
def download_financial_health():
    return send_from_directory(
        BASE_DIR / "output",
        "financial_health.xlsx",
        as_attachment=True
    )


@app.route("/download/cashflow")
def download_cashflow():
    return send_from_directory(
        BASE_DIR / "output",
        "cashflow_intelligence.xlsx",
        as_attachment=True
    )


@app.route("/download/earnings")
def download_earnings():
    return send_from_directory(
        BASE_DIR / "output",
        "earnings_quality.xlsx",
        as_attachment=True
    )


@app.route("/download/recommendations")
def download_recommendations():
    return send_from_directory(
        BASE_DIR / "output",
        "investment_recommendations.xlsx",
        as_attachment=True
    )


@app.route("/download/distress")
def download_distress():
    return send_from_directory(
        BASE_DIR / "output",
        "distress_alerts.csv",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)