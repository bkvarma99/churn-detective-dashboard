import sqlite3
import pandas as pd

# Connect to the database we already built
conn = sqlite3.connect("churn.db")

# Make pandas print full width so nothing gets cut off
pd.set_option("display.width", 120)

# ---------------------------------------------------------
# QUERY 1: Churn rate by plan type
# ---------------------------------------------------------
q1 = """
SELECT
    plan_type,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(100.0 * SUM(churned) / COUNT(*), 1) AS churn_rate_pct
FROM customers
GROUP BY plan_type
ORDER BY churn_rate_pct DESC
"""
print("=== 1. Churn Rate by Plan Type ===")
print(pd.read_sql(q1, conn), "\n")

# ---------------------------------------------------------
# QUERY 2: Churn rate by support ticket volume
# ---------------------------------------------------------
q2 = """
SELECT
    support_tickets,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(100.0 * SUM(churned) / COUNT(*), 1) AS churn_rate_pct
FROM customers
GROUP BY support_tickets
ORDER BY support_tickets
"""
print("=== 2. Churn Rate by Support Ticket Count ===")
print(pd.read_sql(q2, conn), "\n")

# ---------------------------------------------------------
# QUERY 3: Revenue at risk (monthly $ lost from churned customers)
# ---------------------------------------------------------
q3 = """
SELECT
    ROUND(SUM(monthly_charge), 2) AS monthly_revenue_lost
FROM customers
WHERE churned = 1
"""
print("=== 3. Monthly Revenue Lost to Churn ===")
print(pd.read_sql(q3, conn), "\n")

# ---------------------------------------------------------
# QUERY 4: Churn rate for missing vs. known login data
# ---------------------------------------------------------
q4 = """
SELECT
    login_data_missing,
    COUNT(*) AS total_customers,
    SUM(churned) AS churned_customers,
    ROUND(100.0 * SUM(churned) / COUNT(*), 1) AS churn_rate_pct
FROM customers
GROUP BY login_data_missing
"""
print("=== 4. Churn Rate: Missing vs. Known Login Data ===")
print(pd.read_sql(q4, conn), "\n")

# ---------------------------------------------------------
# QUERY 5: Average tenure — churned vs retained
# ---------------------------------------------------------
q5 = """
SELECT
    churned,
    ROUND(AVG(tenure_days), 0) AS avg_tenure_days
FROM customers
GROUP BY churned
"""
print("=== 5. Average Tenure: Churned vs Retained ===")
print(pd.read_sql(q5, conn), "\n")

conn.close()