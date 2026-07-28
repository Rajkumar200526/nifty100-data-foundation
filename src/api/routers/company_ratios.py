from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()

@router.get("/company/{company_id}/ratios")
def get_company_ratios(company_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
    """, (company_id,))

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data