import sqlite3


def test_financial_ratios_table_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='financial_ratios'
    """)

    assert cursor.fetchone() is not None

    conn.close()