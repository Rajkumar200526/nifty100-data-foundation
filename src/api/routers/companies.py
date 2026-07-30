from fastapi import APIRouter, HTTPException
from src.api.database import get_connection
import pandas as pd
from pathlib import Path

router = APIRouter()


@router.get("/companies")
def get_companies():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_id,
            company_name
        FROM companies
        ORDER BY company_name
    """)

    companies = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return companies


@router.get("/companies/{company_id}")
def get_company(company_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM companies
        WHERE company_id = ?
    """, (company_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    company = dict(row)

    csv_path = Path("output/company_scores.csv")

    if csv_path.exists():

        df = pd.read_csv(csv_path)

        score = df[df["company_id"] == company_id]

        if not score.empty:

            company["investment_score"] = float(score.iloc[0]["Investment Score"])
            company["recommendation"] = score.iloc[0]["Recommendation"]
            company["rank"] = int(score.iloc[0]["Rank"])

    return company