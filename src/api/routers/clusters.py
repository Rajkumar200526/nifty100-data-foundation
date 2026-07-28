from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/clusters")
def get_clusters():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_id,
            company_name,
            cluster,
            cluster_name
        FROM company_clusters
        ORDER BY cluster, company_name
    """)

    data = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return data