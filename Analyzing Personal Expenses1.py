#import sys
#import subprocess

# Define the packages to be installed
#packages = ["faker", "plotly"]

# Use subprocess to run the pip install command
#for package in packages:
    #subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# The script can continue from here, assuming the packages are now installed
#print("Packages installed successfully.")

#pip install pandas faker
#streamlit run "Analyzing Personal Expenses1.py"


import pandas as pd
import random
from faker import Faker
from datetime import datetime
import calendar
import os

# -----------------------------
# Setup
# -----------------------------

# Initialize Faker and random seed
fake = Faker()
random.seed(42)
Faker.seed(42)

# Output directory for CSV files
output_dir = "monthly_expense_data"
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# Define Expense Categories and Payment Modes
# -----------------------------

categories = {
    "Food": (100, 500),
    "Travel": (500, 5000),
    "Bills": (200, 1500),
    "Groceries": (300, 2000),
    "Subscriptions": (100, 1000),
    "Entertainment": (200, 2000),
    "Gifts": (100, 1500),
    "Shopping": (500, 5000),
    "Healthcare": (300, 2500),
    "Education": (1000, 8000)
}

payment_modes = ["Cash", "UPI", "Credit Card", "Debit Card", "Netbanking"]

# -----------------------------
# Generate Expense Data for Each Month
# -----------------------------

year = 2025

for month in range(1, 13):  # Loop from January to December
    month_data = []
    _, days_in_month = calendar.monthrange(year, month)

    num_transactions = random.randint(80, 120)  # Number of transactions per month

    for _ in range(num_transactions):
        category = random.choice(list(categories.keys()))
        min_amt, max_amt = categories[category]
        amount = round(random.uniform(min_amt, max_amt), 2)

        # 30% chance to receive cashback
        cashback = round(random.uniform(0, amount * 0.1), 2) if random.random() < 0.3 else 0.0

        transaction = {
            "Date": fake.date_between(start_date=datetime(year, month, 1), 
                                      end_date=datetime(year, month, days_in_month)),
            "Category": category,
            "Payment_Mode": random.choice(payment_modes),
            "Description": fake.sentence(nb_words=4),
            "Amount_Paid": amount,
            "Cashback": cashback
        }

        month_data.append(transaction)

    # Convert to DataFrame
    df = pd.DataFrame(month_data)

    # Save CSV
    month_name = calendar.month_name[month]
    filename = f"{output_dir}/{month_name}_2025.csv"
    df.to_csv(filename, index=False)

    print(f"[✓] {month_name} 2025 - {len(df)} records saved to {filename}")


#python generate_expense_data.py
