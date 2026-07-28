from fastapi import APIRouter, Query
from src.api.database import get_connection

router = APIRouter()


@router.get("/search")
def search_company(name: str = Query(...)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_id,
            company_name
        FROM companies
        WHERE company_name LIKE ?
        ORDER BY company_name
    """, (f"%{name}%",))

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return data