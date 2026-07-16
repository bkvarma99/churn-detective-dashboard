import sqlite3
import pandas as pd

# Step 1: Load our clean CSV data
df = pd.read_csv("clean_customers.csv")

# Step 2: Create (or connect to) a database file called churn.db
# Think of this as creating a brand-new empty filing cabinet.
conn = sqlite3.connect("churn.db")

# Step 3: Save our data into a table inside that filing cabinet,
# called "customers". if_exists="replace" means: if we run this
# script again, start fresh instead of duplicating everything.
df.to_sql("customers", conn, if_exists="replace", index=False)

# Step 4: Let's prove it worked by asking SQL a simple question:
# "How many rows are in the customers table?"
result = pd.read_sql("SELECT COUNT(*) AS total_customers FROM customers", conn)
print("Total customers loaded into SQL database:")
print(result)

# Step 5: Let's ask a slightly more interesting question:
# "How many customers churned vs. stayed?"
result2 = pd.read_sql("""
    SELECT churned, COUNT(*) AS num_customers
    FROM customers
    GROUP BY churned
""", conn)
print("\nChurn breakdown:")
print(result2)

conn.close()
print("\nDone! Your data now lives in churn.db")