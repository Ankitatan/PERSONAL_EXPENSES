import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

DB_PATH = "expenses.db"

# ---------------- DATABASE FUNCTIONS -----------------
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_table():
    conn = get_connection()
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

def load_expenses():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df

def insert_expense(date, category, payment_mode, desc, amount, cashback):
    conn = get_connection()
    conn.execute("""
        INSERT INTO expenses (date, category, payment_mode, description, amount, cashback)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, category, payment_mode, desc, amount, cashback))
    conn.commit()
    conn.close()


# ---------------- APP CONFIG -------------------------
st.set_page_config(page_title="Advanced Expense Dashboard", layout="wide")

# ----- CUSTOM CSS for MAROON ACTIVE TAB -----
# ---------------- CUSTOM CSS FOR TABS -----------------
st.markdown(
    """
    <style>
    /* Inactive tabs: light blue background, blue text, rounded, padding, border */
    div[data-baseweb="tab-list"] button {
        background-color: #87CEEB;   /* Light Sky Blue */
        color: #104E8B;               /* Dark Blue text */
        border-radius: 12px;         
        padding: 10px 20px;          
        border: 2px solid #104E8B;  
        font-weight: bold;           
        margin-right: 4px;           
        transition: all 0.3s ease;   
    }

    /* Active tab: white background, blue text, blue border */
    div[data-baseweb="tab-list"] button[data-selected="true"] {
        background-color: white;     
        color: #104E8B !important;   
        border-radius: 12px;
        padding: 10px 20px;
        border: 2px solid #104E8B;  
        font-weight: bold;
        transition: all 0.3s ease;   
    }

    /* Hover effect for inactive tabs */
    div[data-baseweb="tab-list"] button:hover {
        background-color: #104E8B;  
        color: white;
        transition: all 0.3s ease;   
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💰 ADVANCED PERSONAL EXPENSE DASHBOARD")
st.write("Analyze your expenses with SQL-powered insights, filters, charts & KPIs.")

create_table()
df = load_expenses()

# ---------------- FILTER SIDEBAR -------------------
st.sidebar.header("🔍 Filters")

if not df.empty:
    categories = ["All"] + sorted(df["category"].unique().tolist())
    payment_modes = ["All"] + sorted(df["payment_mode"].unique().tolist())

    selected_category = st.sidebar.selectbox("Filter by Category:", categories)
    selected_payment = st.sidebar.selectbox("Filter by Payment Mode:", payment_modes)
    selected_month = st.sidebar.selectbox("Filter by Month:",
                                          ["All"] + sorted(df['date'].str.slice(0, 7).unique().tolist()))

    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    if selected_payment != "All":
        filtered_df = filtered_df[filtered_df["payment_mode"] == selected_payment]
    if selected_month != "All":
        filtered_df = filtered_df[filtered_df["date"].str.startswith(selected_month)]
else:
    filtered_df = pd.DataFrame()


# -------------------- TABS ------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Dashboard", "🧮 SQL Insights", "➕ Add Expense",
     "📄 Raw Data", "⬇️ Download"]
)

# ---------------- TAB 1 — DASHBOARD ----------------
with tab1:
    st.header("📊 Expense Overview")

    if filtered_df.empty:
        st.warning("No data available. Add records in 'Add Expense' tab.")
    else:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Spending", f"₹{filtered_df['amount'].sum():,.2f}", delta_color="inverse")
        col2.metric("Transactions", len(filtered_df))
        col3.metric("Total Cashback", f"₹{filtered_df['cashback'].sum():,.2f}", delta_color="inverse")
        col4.metric("Avg Transaction", f"₹{filtered_df['amount'].mean():,.2f}", delta_color="inverse")

        # Category Chart
        st.subheader("📌 Spending by Category")
        cat_data = filtered_df.groupby("category")["amount"].sum().reset_index()
        st.bar_chart(cat_data, x="category", y="amount")

        # Payment Mode Pie Chart
        st.subheader("💳 Payment Mode Distribution")
        pm_data = filtered_df.groupby("payment_mode")["amount"].sum().reset_index()
        fig = px.pie(pm_data, names="payment_mode", values="amount")
        st.plotly_chart(fig)

        # Monthly Trend
        st.subheader("📅 Monthly Spending Trend")
        filtered_df["month"] = filtered_df["date"].str.slice(0, 7)
        trend = filtered_df.groupby("month")["amount"].sum().reset_index()
        st.line_chart(trend, x="month", y="amount")


# ---------------- TAB 2 — SQL INSIGHTS ----------------
with tab2:
    st.header("🧮 SQL Analytics")
    if df.empty:
        st.warning("Add some expenses to view SQL insights.")
    else:
        conn = get_connection()
        queries = {
            "Total spending by category":
                "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category",

            "Spending by payment mode":
                "SELECT payment_mode, SUM(amount) AS total FROM expenses GROUP BY payment_mode",

            "Top 5 expensive categories":
                "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC LIMIT 5",

            "Total cashback earned":
                "SELECT SUM(cashback) AS cashback FROM expenses",

            "Monthly spending":
                "SELECT SUBSTR(date,1,7) AS month, SUM(amount) FROM expenses GROUP BY month",

            "Transactions with cashback":
                "SELECT * FROM expenses WHERE cashback > 0",

            "Highest spending category %":
                "SELECT category, SUM(amount)*100.0 / (SELECT SUM(amount) FROM expenses) AS percentage FROM expenses GROUP BY category ORDER BY percentage DESC LIMIT 1",

            "Recurring expenses by description":
                "SELECT description, COUNT(*) AS freq FROM expenses GROUP BY description HAVING freq > 2",

            "Travel-related spending":
                "SELECT * FROM expenses WHERE category = 'Travel'",

            "Grocery patterns (monthly)": 
                "SELECT SUBSTR(date,1,7) AS month, SUM(amount) FROM expenses WHERE category='Grocery' GROUP BY month",

            "Cash vs Online detailed":
                "SELECT payment_mode, COUNT(*) AS count, SUM(amount) AS total FROM expenses GROUP BY payment_mode",

            "Max transaction":
                "SELECT * FROM expenses ORDER BY amount DESC LIMIT 1",

            "Min transaction":
                "SELECT * FROM expenses ORDER BY amount ASC LIMIT 1",

            "Average monthly spend":
                "SELECT AVG(monthly) FROM (SELECT SUBSTR(date,1,7) AS m, SUM(amount) AS monthly FROM expenses GROUP BY m)"
        }
        selected_query = st.selectbox("Select a query to run:", list(queries.keys()))
        if st.button("Run Query"):
            result = pd.read_sql_query(queries[selected_query], conn)
            st.dataframe(result, use_container_width=True)
        conn.close()


# ---------------- TAB 3 — ADD EXPENSE ----------------
with tab3:
    st.header("➕ Add New Expense")
    date = st.date_input("Date")
    category = st.text_input("Category")
    payment = st.selectbox("Payment Mode", ["Cash", "Online"])
    desc = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0)
    cashback = st.number_input("Cashback", min_value=0.0)

    if st.button("Add Expense"):
        insert_expense(str(date), category, payment, desc, amount, cashback)
        st.success("Expense added successfully!")


# ---------------- TAB 4 — RAW DATA ----------------
with tab4:
    st.header("📄 Raw Expense Data")
    if df.empty:
        st.warning("No expense data available.")
    else:
        st.dataframe(df, use_container_width=True)


# ---------------- TAB 5 — DOWNLOAD ----------------
with tab5:
    st.header("⬇️ Download Your Data")
    if df.empty:
        st.warning("Nothing to download.")
    else:
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "expenses.csv", "text/csv")
