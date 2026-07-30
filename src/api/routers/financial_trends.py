from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter()


@router.get("/financial-trends/{company_id}")
def financial_trends(company_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        c.company_name,
        fr.year,
        fr.sales,
        fr.net_profit,
        fr.operating_profit,
        fr.roe,
        fr.roce,
        fr.free_cash_flow
    FROM financial_ratios fr
    INNER JOIN companies c
        ON fr.company_id = c.company_id
    WHERE fr.company_id = ?
    ORDER BY fr.year
""", (company_id,))

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Financial trends not found"
        )

    return data