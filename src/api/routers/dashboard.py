from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/dashboard")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    total_companies = cursor.execute(
        "SELECT COUNT(*) FROM companies"
    ).fetchone()[0]

    total_clusters = cursor.execute(
        "SELECT COUNT(DISTINCT cluster) FROM company_clusters"
    ).fetchone()[0]

    avg_roe = cursor.execute(
        "SELECT ROUND(AVG(roe),2) FROM financial_ratios WHERE year=2024"
    ).fetchone()[0]

    conn.close()

    return {
        "total_companies": total_companies,
        "total_clusters": total_clusters,
        "average_roe": avg_roe
    }