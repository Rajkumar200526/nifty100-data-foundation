from fastapi import APIRouter, HTTPException
from src.api.database import get_connection

router = APIRouter()


@router.get("/recommendation/{company_id}")
def recommendation(company_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_name,
            year,
            roe,
            roce,
            debt_to_equity,
            free_cash_flow
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC
        LIMIT 1
    """, (company_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    company = dict(row)

    score = 0

    if company["roe"] >= 20:
        score += 1

    if company["roce"] >= 20:
        score += 1

    if company["debt_to_equity"] <= 1:
        score += 1

    if company["free_cash_flow"] > 0:
        score += 1

    if score == 4:
        recommendation = "BUY"
    elif score >= 2:
        recommendation = "HOLD"
    else:
        recommendation = "WATCH"

    company["score"] = score
    company["recommendation"] = recommendation

    return company