# Save this code in a Python script to generate the SQL query file

-- 1. Total amount spent in each category
SELECT category, SUM(amount_paid) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC;

-- 2. Total amount spent using each payment mode
SELECT payment_mode, SUM(amount_paid) AS total_spent
FROM expenses
GROUP BY payment_mode;

-- 3. Total cashback received across all transactions
SELECT SUM(cashback) AS total_cashback
FROM expenses;

-- 4. Top 5 most expensive categories in terms of spending
SELECT category, SUM(amount_paid) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC
LIMIT 5;

-- 5. Amount spent on transportation using different payment modes
SELECT payment_mode, SUM(amount_paid) AS total_spent
FROM expenses
WHERE category = 'Transportation'
GROUP BY payment_mode;

-- 6. Transactions that resulted in cashback
SELECT *
FROM expenses
WHERE cashback > 0;

-- 7. Total spending in each month of the year
SELECT MONTH(date) AS month, SUM(amount_paid) AS total_spent
FROM expenses
GROUP BY MONTH(date)
ORDER BY month;

-- 8. Highest spending months for Travel, Entertainment, or Gifts
SELECT MONTH(date) AS month, category, SUM(amount_paid) AS total_spent
FROM expenses
WHERE category IN ('Travel', 'Entertainment', 'Gifts')
GROUP BY MONTH(date), category
ORDER BY total_spent DESC;

-- 9. Recurring expenses in specific months (e.g., insurance, property taxes)
SELECT MONTH(date) AS month, category, COUNT(*) AS frequency
FROM expenses
WHERE category IN ('Insurance', 'Bills')
GROUP BY MONTH(date), category
ORDER BY frequency DESC;

-- 10. Cashback or rewards earned in each month
SELECT MONTH(date) AS month, SUM(cashback) AS total_cashback
FROM expenses
GROUP BY MONTH(date)
ORDER BY month;

-- 11. Overall spending trend (monthly)
SELECT MONTH(date) AS month, SUM(amount_paid) AS total_spent
FROM expenses
GROUP BY MONTH(date)
ORDER BY month;

-- 12. Costs associated with different travel types (assuming description field)
SELECT description, AVG(amount_paid) AS avg_cost
FROM expenses
WHERE category = 'Travel'
GROUP BY description
ORDER BY avg_cost DESC;

-- 13. Grocery spending patterns (weekends vs weekdays)
SELECT 
    CASE 
        WHEN DAYOFWEEK(date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    AVG(amount_paid) AS avg_spent
FROM expenses
WHERE category = 'Groceries'
GROUP BY day_type;

-- 14. High vs Low Priority Categories
SELECT category, SUM(amount_paid) AS total_spent,
       CASE 
           WHEN category IN ('Bills', 'Insurance', 'Health') THEN 'High Priority'
           ELSE 'Low Priority'
       END AS priority
FROM expenses
GROUP BY category, priority
ORDER BY total_spent DESC;

-- 15. Category contributing highest percentage of total spending
SELECT category, 
       SUM(amount_paid) AS category_spent,
       (SUM(amount_paid) / (SELECT SUM(amount_paid) FROM expenses) * 100) AS percent_total
FROM expenses
GROUP BY category
ORDER BY percent_total DESC
LIMIT 1;

-- 16. Average transaction amount per category
SELECT category, AVG(amount_paid) AS avg_spent
FROM expenses
GROUP BY category;

-- 17. Minimum and maximum amount spent per category
SELECT category, MIN(amount_paid) AS min_spent, MAX(amount_paid) AS max_spent
FROM expenses
GROUP BY category;

-- 18. Most frequent transaction category
SELECT category, COUNT(*) AS num_transactions
FROM expenses
GROUP BY category
ORDER BY num_transactions DESC
LIMIT 1;

-- 19. Average cashback by payment mode
SELECT payment_mode, AVG(cashback) AS avg_cashback
FROM expenses
GROUP BY payment_mode;

-- 20. Weekend vs Weekday total spending
SELECT 
    CASE 
        WHEN DAYOFWEEK(date) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    SUM(amount_paid) AS total_spent
FROM expenses
GROUP BY day_type;

-- 21. Monthly average spending
SELECT MONTH(date) AS month, AVG(amount_paid) AS avg_spent
FROM expenses
GROUP BY MONTH(date);

-- 22. Most common vendors/expenses (based on description)
SELECT description, COUNT(*) AS frequency
FROM expenses
GROUP BY description
ORDER BY frequency DESC
LIMIT 5;

-- 23. Highest cashback months
SELECT MONTH(date) AS month, SUM(cashback) AS total_cashback
FROM expenses
GROUP BY MONTH(date)
ORDER BY total_cashback DESC;

-- 24. Compare first half vs second half of the year
SELECT 
    CASE 
        WHEN MONTH(date) <= 6 THEN 'H1'
        ELSE 'H2'
    END AS half_year,
    SUM(amount_paid) AS total_spent
FROM expenses
GROUP BY half_year;

-- 25. Monthly trend of online vs cash payments
SELECT MONTH(date) AS month, 
       SUM(CASE WHEN payment_mode = 'Cash' THEN amount_paid ELSE 0 END) AS cash_spent,
       SUM(CASE WHEN payment_mode != 'Cash' THEN amount_paid ELSE 0 END) AS online_spent
FROM expenses
GROUP BY MONTH(date)
ORDER BY month;


# Write the SQL to a file
# with open("expense_tracker_queries.sql", "w") as file:
 #   file.write(queries)
