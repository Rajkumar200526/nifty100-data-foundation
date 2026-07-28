from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/top-performers")
def top_performers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.company_name,
            f.year,
            ROUND(f.roe, 2) AS roe,
            ROUND(f.roce, 2) AS roce
        FROM financial_ratios f
        JOIN companies c
            ON f.company_id = c.company_id
        WHERE f.year = 2024
        ORDER BY f.roe DESC
        LIMIT 10
    """)

    data = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return data