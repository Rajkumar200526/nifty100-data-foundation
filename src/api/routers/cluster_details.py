from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/cluster/{cluster_id}")
def get_cluster(cluster_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_id,
            company_name,
            cluster,
            cluster_name
        FROM company_clusters
        WHERE cluster = ?
        ORDER BY company_name
    """, (cluster_id,))

    data = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return data