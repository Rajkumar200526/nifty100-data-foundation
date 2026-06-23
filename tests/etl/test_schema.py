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