import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# This makes our "random" fake data the same every time we run it,
# so you and I see identical results when troubleshooting.
random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

NUM_CUSTOMERS = 2000

# Realistic plan names written INCONSISTENTLY on purpose (our messiness!)
plan_variants = {
    "Basic": ["Basic", "basic", "BASIC", "Basic "],
    "Premium": ["Premium", "premium", "PREM", "Premiun", "Premium "],
    "Pro": ["Pro", "pro", "PRO", "Pro "]
}
plan_base_price = {"Basic": 9.99, "Premium": 19.99, "Pro": 39.99}

rows = []
today = datetime.now()

for i in range(NUM_CUSTOMERS):
    customer_id = 1000 + i
    name = fake.name()
    email = fake.email()

    plan_key = random.choice(list(plan_variants.keys()))
    plan_written = random.choice(plan_variants[plan_key])  # messy version
    monthly_charge = plan_base_price[plan_key]

    signup_date = fake.date_between(start_date="-2y", end_date="-1M")

    # Glitch #1: ~5% of rows have a MISSING last login date
    if random.random() < 0.05:
        last_login = None
    else:
        last_login = fake.date_between(start_date=signup_date, end_date=today.date())

    support_tickets = np.random.poisson(1.2)
    tenure_days = (today.date() - signup_date).days

    # Customers who haven't logged in for 45+ days are more likely to have churned
    days_since_login = (today.date() - last_login).days if last_login else 999
    churn_prob = 0.05 + (0.5 if days_since_login > 45 else 0) + (0.1 * support_tickets if support_tickets > 2 else 0)
    churned = 1 if random.random() < min(churn_prob, 0.95) else 0

    rows.append({
        "customer_id": customer_id,
        "name": name,
        "email": email,
        "plan_type": plan_written,
        "monthly_charge": monthly_charge,
        "signup_date": signup_date,
        "last_login_date": last_login,
        "support_tickets": support_tickets,
        "tenure_days": tenure_days,
        "churned": churned
    })

df = pd.DataFrame(rows)

# Glitch #2: DUPLICATE customers — pick 3% of customers and duplicate their row
dupe_sample = df.sample(frac=0.03, random_state=42)
df = pd.concat([df, dupe_sample], ignore_index=True)

# Shuffle so duplicates aren't neatly stacked (more realistic)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to a CSV file (like an Excel file, but simpler) in our project folder
df.to_csv("raw_customers.csv", index=False)

print("Done! Created raw_customers.csv with", len(df), "rows (including duplicates).")
print("Here's a sneak peek of the first 5 rows:")
print(df.head())