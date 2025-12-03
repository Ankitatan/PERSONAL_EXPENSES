# analytics_queries.py
def wrap_where(where_clause: str) -> str:
    """Return formatted WHERE addition (SQLite). Pass empty string if none."""
    where_clause = (where_clause or "").strip()
    if where_clause == "":
        return ""
    # If user passed a condition starting with AND, keep it.
    if where_clause.upper().startswith("AND "):
        return " " + where_clause
    # otherwise prepend AND to combine with existing base WHERE
    return " AND " + where_clause

def total_by_category(where_clause: str = "") -> str:
    return f"""
    SELECT category, ROUND(SUM(amount),2) AS total_spent, COUNT(*) AS txn_count
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY category
    ORDER BY total_spent DESC;
    """

def total_by_payment_mode(where_clause: str = "") -> str:
    return f"""
    SELECT payment_mode, ROUND(SUM(amount),2) AS total_spent, COUNT(*) AS txn_count
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY payment_mode;
    """

def total_cashback(where_clause: str = "") -> str:
    return f"SELECT ROUND(SUM(cashback),2) AS total_cashback FROM expenses WHERE 1=1 {wrap_where(where_clause)};"

def monthly_spending(where_clause: str = "") -> str:
    # month as integer
    return f"""
    SELECT CAST(strftime('%m', date) AS INTEGER) AS month,
           ROUND(SUM(amount),2) AS total_spent
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY month
    ORDER BY month;
    """

def top_categories(limit: int = 5, where_clause: str = "") -> str:
    return f"""
    SELECT category, ROUND(SUM(amount),2) AS total_spent
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY category
    ORDER BY total_spent DESC
    LIMIT {int(limit)};
    """

def transport_by_payment(where_clause: str = "") -> str:
    return f"""
    SELECT payment_mode, ROUND(SUM(amount),2) AS total_spent
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)} AND category = 'Transportation'
    GROUP BY payment_mode;
    """

def cashback_transactions(limit: int = 200, where_clause: str = "") -> str:
    return f"""
    SELECT id, date, category, payment_mode, amount, cashback
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)} AND cashback > 0
    ORDER BY cashback DESC
    LIMIT {int(limit)};
    """

def months_for_categories(categories: list, where_clause: str = "") -> str:
    # categories is list of strings
    cats = ",".join([f"'{c}'" for c in categories])
    return f"""
    SELECT CAST(strftime('%m', date) AS INTEGER) AS month, category, ROUND(SUM(amount),2) AS total_spent
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)} AND category IN ({cats})
    GROUP BY month, category
    ORDER BY month, total_spent DESC;
    """

def recurring_expenses(min_occurrences: int = 2, where_clause: str = "") -> str:
    # recurring inferred by identical description (if available) or repeated category+amount combos.
    # Our basic schema doesn't include description; show recurring by category-month frequency.
    return f"""
    SELECT category, COUNT(*) AS occurrences, GROUP_CONCAT(DISTINCT CAST(strftime('%m', date) AS INTEGER)) AS months
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY category
    HAVING occurrences >= {int(min_occurrences)}
    ORDER BY occurrences DESC;
    """

def monthly_cashback(where_clause: str = "") -> str:
    return f"""
    SELECT CAST(strftime('%m', date) AS INTEGER) AS month, ROUND(SUM(cashback),2) AS total_cashback
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY month
    ORDER BY month;
    """

def category_contribution_pct(where_clause: str = "") -> str:
    return f"""
    SELECT category,
           ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM expenses WHERE 1=1 {wrap_where(where_clause)}),2) AS pct_contribution,
           ROUND(SUM(amount),2) AS total_spent
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY category
    ORDER BY pct_contribution DESC;
    """

# Extra queries
def avg_txn_by_category(where_clause: str = "") -> str:
    return f"""
    SELECT category, ROUND(AVG(amount),2) AS avg_amount, COUNT(*) AS txn_count
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY category
    ORDER BY avg_amount DESC;
    """

def top_transactions(limit: int = 10, where_clause: str = "") -> str:
    return f"""
    SELECT id, date, category, payment_mode, amount
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    ORDER BY amount DESC
    LIMIT {int(limit)};
    """

def weekday_spending(where_clause: str = "") -> str:
    # SQLite strftime('%w') 0 = Sunday ... 6 = Saturday
    return f"""
    SELECT CAST(strftime('%w', date) AS INTEGER) AS weekday, ROUND(SUM(amount),2) AS total_spent, COUNT(*) AS txn_count
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY weekday
    ORDER BY weekday;
    """

def compare_h1_h2(where_clause: str = "") -> str:
    return f"""
    SELECT CASE WHEN CAST(strftime('%m', date) AS INTEGER) <= 6 THEN 'H1' ELSE 'H2' END AS half,
           ROUND(SUM(amount),2) AS total_spent
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY half;
    """
def h1_vs_h2_spending(where_clause: str = "") -> str:
    return f"""
    SELECT CASE WHEN CAST(strftime('%m', date) AS INTEGER) <=6 THEN 'H1' ELSE 'H2' END AS half,
           ROUND(SUM(amount),2) AS total_spent
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    GROUP BY half;
    """

def grocery_weekend_pattern(where_clause: str = "") -> str:
    return f"""
    SELECT CASE WHEN CAST(strftime('%w', date) AS INTEGER) IN (0,6) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
           ROUND(SUM(amount),2) AS total_spent
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)} AND category='Grocery'
    GROUP BY day_type;
    """

def category_contribution(where_clause: str = "") -> str:
    return f"""
    SELECT category,
           ROUND(SUM(amount)*100.0 / (SELECT SUM(amount) FROM expenses WHERE 1=1 {wrap_where(where_clause)}),2) AS pct_contribution,
           ROUND(SUM(amount),2) AS total_spent
    FROM expenses
    WHERE 1=1 {wrap_where(where_clause)}
    ORDER BY pct_contribution DESC;
    """
