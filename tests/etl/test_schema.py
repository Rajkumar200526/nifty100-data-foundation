import sqlite3

def test_companies_table_exists():

    conn = sqlite3.connect("db/nifty100.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name='companies'
    """)

    result = cursor.fetchone()

    conn.close()

    assert result is not None
import sqlite3


def get_tables():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """)

    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    return tables


def test_companies_exists():
    assert "companies" in get_tables()


def test_sectors_exists():
    assert "sectors" in get_tables()


def test_financial_ratios_exists():
    assert "financial_ratios" in get_tables()


def test_profitandloss_exists():
    assert "profitandloss" in get_tables()


def test_balancesheet_exists():
    assert "balancesheet" in get_tables()


def test_cashflow_exists():
    assert "cashflow" in get_tables()


def test_stock_prices_exists():
    assert "stock_prices" in get_tables()