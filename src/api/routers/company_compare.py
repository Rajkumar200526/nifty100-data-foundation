from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter()


@router.get("/compare")
def compare_companies(company1: int, company2: int):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1
    """

    # First company
    cursor.execute(query, (company1,))
    company_a = cursor.fetchone()

    # Second company
    cursor.execute(query, (company2,))
    company_b = cursor.fetchone()

    conn.close()

    if not company_a or not company_b:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return {
        "company1": dict(company_a),
        "company2": dict(company_b)
    }