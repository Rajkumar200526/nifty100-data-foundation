import sqlite3

DB_PATH = "db/nifty100.db"


def get_connection():
    """
    Returns a connection to the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn