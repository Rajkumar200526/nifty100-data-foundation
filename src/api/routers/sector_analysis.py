from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/sector-analysis")
def sector_analysis():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.broad_sector AS sector,
            COUNT(DISTINCT c.company_id) AS companies,
            AVG(fr.sales) AS avg_sales,
            AVG(fr.net_profit) AS avg_profit,
            AVG(fr.roe) AS avg_roe
        FROM companies c
        JOIN financial_ratios fr
            ON c.company_id = fr.company_id
        GROUP BY c.broad_sector
        ORDER BY companies DESC
    """)

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append({
            "sector": row["sector"],
            "companies": row["companies"],
            "avg_sales": round(row["avg_sales"], 2),
            "avg_profit": round(row["avg_profit"], 2),
            "avg_roe": round(row["avg_roe"], 2)
        })

    conn.close()

    return data