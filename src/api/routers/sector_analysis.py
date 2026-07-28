from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/sector-analysis")
def sector_analysis():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            broad_sector,
            COUNT(*) AS total_companies
        FROM companies
        GROUP BY broad_sector
        ORDER BY total_companies DESC
    """)

    data = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return data