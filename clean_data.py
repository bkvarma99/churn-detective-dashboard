import pandas as pd

# Step 1: Load the messy data we created earlier
df = pd.read_csv("raw_customers.csv")
print("Starting rows:", len(df))

# ---------------------------------------------------------
# FIX #1: Standardize inconsistent plan_type text
# ---------------------------------------------------------
# First, remove extra spaces and make everything lowercase
# so "Premium ", "PREMIUM", "premium" all become "premium"
df["plan_type"] = df["plan_type"].str.strip().str.lower()

# Now map every messy spelling to one clean, correct name
plan_cleanup_map = {
    "basic": "Basic",
    "premium": "Premium",
    "premiun": "Premium",   # typo fix!
    "prem": "Premium",      # abbreviation fix!
    "pro": "Pro"
}
df["plan_type"] = df["plan_type"].map(plan_cleanup_map)

print("\nUnique plan types after cleaning:")
print(df["plan_type"].value_counts())

# ---------------------------------------------------------
# FIX #2: Remove duplicate customers
# ---------------------------------------------------------
# If the same customer_id appears more than once, keep only
# the FIRST occurrence and drop the rest.
before_dedupe = len(df)
df = df.drop_duplicates(subset="customer_id", keep="first")
after_dedupe = len(df)

print(f"\nRemoved {before_dedupe - after_dedupe} duplicate customer rows.")

# ---------------------------------------------------------
# FIX #3: Handle missing last_login_date honestly
# ---------------------------------------------------------
# Instead of guessing a fake date, we flag it clearly.
df["login_data_missing"] = df["last_login_date"].isna()

missing_count = df["login_data_missing"].sum()
print(f"\nFlagged {missing_count} rows with missing last_login_date.")

# ---------------------------------------------------------
# Save the cleaned file
# ---------------------------------------------------------
df.to_csv("clean_customers.csv", index=False)
print(f"\nDone! Saved clean_customers.csv with {len(df)} clean rows.")