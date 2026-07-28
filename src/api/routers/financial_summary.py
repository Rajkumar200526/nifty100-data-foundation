from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter()


@router.get("/financial-summary/{company_id}")
def financial_summary(company_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_name,
            year,
            sales,
            net_profit,
            operating_profit,
            roe,
            roce,
            free_cash_flow
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
    """, (company_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Financial summary not found"
        )

    return dict(row)