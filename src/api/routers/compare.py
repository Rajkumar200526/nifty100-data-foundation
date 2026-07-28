from fastapi import APIRouter, Query
from src.api.database import get_connection

router = APIRouter()


@router.get("/compare")
def compare_companies(
    company1: int = Query(...),
    company2: int = Query(...)
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_id,
            company_name,
            year,
            sales,
            net_profit,
            operating_profit,
            roe,
            roce,
            debt_to_equity,
            free_cash_flow
        FROM financial_ratios
        WHERE company_id IN (?, ?)
          AND year = 2024
        ORDER BY company_name
    """, (company1, company2))

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data