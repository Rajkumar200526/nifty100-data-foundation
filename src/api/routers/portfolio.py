from fastapi import APIRouter, Query
from src.api.database import get_connection
import pandas as pd
from pathlib import Path

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parents[3]
OUTPUT_DIR = BASE_DIR / "output"


@router.get("/portfolio")
def portfolio_summary(companies: str = Query(...)):
    company_ids = [
        int(company_id.strip())
        for company_id in companies.split(",")
    ]

    placeholders = ",".join(["?"] * len(company_ids))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            COUNT(*) AS total_companies,
            SUM(sales) AS total_sales,
            SUM(net_profit) AS total_net_profit,
            AVG(roe) AS average_roe,
            AVG(roce) AS average_roce
        FROM financial_ratios
        WHERE company_id IN ({placeholders})
          AND year = 2024
    """, company_ids)

    result = dict(cursor.fetchone())
    

    conn.close()

    return result
@router.post("/portfolio/{company_id}")
def add_to_portfolio(company_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM portfolio WHERE company_id = ?",
        (company_id,)
    )

    if cursor.fetchone():

        conn.close()

        return {
            "message": "Company already added"
        }

    cursor.execute(
        "INSERT INTO portfolio(company_id) VALUES(?)",
        (company_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Company added successfully"
    }
@router.get("/portfolio/list")
def get_portfolio():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.company_id,
            p.added_date
        FROM portfolio p
    """)

    portfolio = cursor.fetchall()
    conn.close()

    if not portfolio:
        return []

    file = OUTPUT_DIR / "company_scores.csv"

    df = pd.read_csv(file)

    df.rename(columns={
        "Investment Score": "investment_score"
    }, inplace=True)

    result = []

    for row in portfolio:

        company = df[df["company_id"] == row["company_id"]]

        if company.empty:
            continue

        company = company.iloc[0]

        result.append({
            "id": row["id"],
            "company_id": row["company_id"],
            "company_name": company["company_name"],
            "broad_sector": company["broad_sector"],
            "investment_score": company["investment_score"],
            "recommendation": company["Recommendation"],
            "added_date": row["added_date"]
        })

    return result
@router.delete("/portfolio/{portfolio_id}")
def remove_from_portfolio(portfolio_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM portfolio WHERE id = ?",
        (portfolio_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Company removed successfully"
    }
@router.get("/portfolio/health")
def portfolio_health():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT company_id
        FROM portfolio
    """)

    portfolio = cursor.fetchall()

    conn.close()

    if not portfolio:
        return {
            "health_score": 0,
            "status": "No Portfolio"
        }

    company_ids = [row["company_id"] for row in portfolio]

    file = OUTPUT_DIR / "company_scores.csv"

    df = pd.read_csv(file)

    df.rename(columns={
        "Investment Score": "investment_score"
    }, inplace=True)

    df = df[df["company_id"].isin(company_ids)]

    avg = round(df["investment_score"].mean(), 2)

    if avg >= 3.5:
        status = "Excellent"
    elif avg >= 2.5:
        status = "Good"
    elif avg >= 1.5:
        status = "Average"
    else:
        status = "High Risk"

    return {
        "health_score": avg,
        "status": status,
        "companies": len(df)
    }
@router.get("/portfolio/insights")
def portfolio_insights():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT company_id
        FROM portfolio
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {
            "message": "Portfolio is empty."
        }

    company_ids = [row["company_id"] for row in rows]

    file = OUTPUT_DIR / "company_scores.csv"

    df = pd.read_csv(file)

    df.rename(columns={
        "Investment Score": "investment_score"
    }, inplace=True)

    df = df[df["company_id"].isin(company_ids)]

    best = df.loc[df["investment_score"].idxmax()]
    worst = df.loc[df["investment_score"].idxmin()]

    top_sector = (
        df["broad_sector"]
        .value_counts()
        .idxmax()
    )

    return {

        "best_company": best["company_name"],

        "best_score": round(best["investment_score"], 2),

        "worst_company": worst["company_name"],

        "worst_score": round(worst["investment_score"], 2),

        "top_sector": top_sector,

        "suggestion":
            f"Consider adding more companies outside the {top_sector} sector to improve diversification."

    }