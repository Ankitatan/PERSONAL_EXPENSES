# data_simulation.py
from faker import Faker
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "expenses.db"
fake = Faker()

categories = [
    "Food", "Groceries", "Bills", "Transportation", "Entertainment",
    "Subscriptions", "Travel", "Health", "Shopping", "Gifts"
]

payment_modes = ["Cash", "Online"]

def get_random_date(year=2025, month=None):
    if month:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year, 12, 31)
        else:
            end_date = datetime(year, month+1, 1) - timedelta(days=1)
    else:
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
    return fake.date_between(start_date=start_date, end_date=end_date)

def generate_expenses(n=1200):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for _ in range(n):
        date = get_random_date(month=random.randint(1,12))
        category = random.choice(categories)
        payment_mode = random.choice(payment_modes)
        desc = f"{category} - {fake.word()}"
        amount = round(random.uniform(50, 5000), 2)
        cashback = round(amount * random.choice([0, 0.02, 0.05]), 2)  # 0%, 2%, or 5%

        cursor.execute("""
        INSERT INTO expenses (date, category, payment_mode, description, amount, cashback)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (str(date), category, payment_mode, desc, amount, cashback))

    conn.commit()
    conn.close()
    print(f"✅ {n} fake expenses added successfully!")

if __name__ == "__main__":
    generate_expenses()
