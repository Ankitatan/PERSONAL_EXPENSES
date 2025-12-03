# init_db.py
import sqlite3

DB_PATH = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        payment_mode TEXT,
        description TEXT,
        amount REAL,
        cashback REAL
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database and expenses table created successfully!")

if __name__ == "__main__":
    init_db()
