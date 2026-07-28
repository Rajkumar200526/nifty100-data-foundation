import sqlite3
import time
from fastapi import APIRouter

router = APIRouter()

START_TIME = time.time()

DB_PATH = "db/nifty100.db"


@router.get("/health")
def health():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = [
        "companies",
        "financial_ratios",
        "balancesheet",
        "profitandloss",
        "cashflow",
        "stock_prices",
        "company_clusters",
        "users"
    ]

    counts = {}

    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            counts[table] = cursor.fetchone()[0]
        except Exception:
            counts[table] = 0

    conn.close()

    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "db_row_counts": counts
    }