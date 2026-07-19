import sqlite3
import pandas as pd
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "db" / "nifty100.db"



def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def run_query(query, params=None):
    conn = get_connection()

    if params is None:
        params = ()

    return pd.read_sql_query(query, conn, params=params)