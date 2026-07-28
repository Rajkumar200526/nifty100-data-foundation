from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter()


@router.get("/financial-trends/{company_id}")
def financial_trends(company_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            year,
            sales,
            net_profit,
            operating_profit,
            roe,
            roce,
            free_cash_flow
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year
    """, (company_id,))

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Financial trends not found"
        )

    return data