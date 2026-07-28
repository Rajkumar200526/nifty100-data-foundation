from fastapi import APIRouter, Query
from src.api.database import get_connection

router = APIRouter()


@router.get("/portfolio")
def portfolio_summary(companies: str = Query(...)):
    company_ids = [
        int(company_id.strip())
        for company_id in companies.split(",")
    ]

    placeholders = ",".join(["?"] * len(company_ids))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            COUNT(*) AS total_companies,
            SUM(sales) AS total_sales,
            SUM(net_profit) AS total_net_profit,
            AVG(roe) AS average_roe,
            AVG(roce) AS average_roce
        FROM financial_ratios
        WHERE company_id IN ({placeholders})
          AND year = 2024
    """, company_ids)

    result = dict(cursor.fetchone())

    conn.close()

    return result