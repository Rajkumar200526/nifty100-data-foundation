from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/analytics")
def analytics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(DISTINCT company_id) AS total_companies,
            COUNT(*) AS total_records,
            AVG(roe) AS average_roe,
            AVG(roce) AS average_roce,
            SUM(sales) AS total_sales,
            SUM(net_profit) AS total_net_profit
        FROM financial_ratios
    """)

    result = dict(cursor.fetchone())

    conn.close()

    return result
@router.get("/sector-analytics")
def sector_analytics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.broad_sector AS sector,
            COUNT(DISTINCT c.company_id) AS companies,
            ROUND(AVG(f.sales),2) AS avg_sales,
            ROUND(AVG(f.net_profit),2) AS avg_profit,
            ROUND(AVG(f.roe),2) AS avg_roe
        FROM financial_ratios f
        JOIN companies c
            ON f.company_id = c.company_id
        GROUP BY c.broad_sector
        ORDER BY c.broad_sector;
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]