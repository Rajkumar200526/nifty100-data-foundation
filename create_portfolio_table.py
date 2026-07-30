import sqlite3

DB_PATH = "db/nifty100.db"

def create_portfolio_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(company_id)
                REFERENCES companies(company_id)
        )
    """)

    conn.commit()
    conn.close()

    print("✅ Portfolio table created successfully!")

if __name__ == "__main__":
    create_portfolio_table()