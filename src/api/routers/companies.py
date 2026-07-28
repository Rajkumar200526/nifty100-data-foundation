from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter()


@router.get("/companies")
def get_companies():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_id,
            company_name
        FROM companies
        ORDER BY company_name
    """)

    companies = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return companies


@router.get("/companies/{company_id}")
def get_company(company_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM companies
        WHERE company_id = ?
    """, (company_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return dict(row)