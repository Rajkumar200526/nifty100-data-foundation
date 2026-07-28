from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/stock-trends/{company_id}")
def stock_trends(company_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            trade_date,
            close_price
        FROM stock_prices
        WHERE company_id = ?
        ORDER BY trade_date
    """, (company_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]