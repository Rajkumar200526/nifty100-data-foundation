import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"


def insert_companies(df):

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "companies",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

    print("Companies Loaded")