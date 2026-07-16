# 🕵️ Subscription Churn Detective Dashboard

An end-to-end data analytics project that simulates a real-world subscription business, 
injects realistic data quality issues, and uncovers actionable churn drivers through 
SQL analysis and an interactive dashboard.

## 📌 Business Problem

Subscription businesses lose significant revenue to customer churn — and it's far more 
expensive to acquire a new customer than to retain an existing one. This project asks: 
**which customers are at risk of leaving, and what early-warning signals predict it?**

## 🧹 Real-World Data Messiness (Intentionally Injected & Solved)

Real corporate data is never clean. This project simulates and resolves three common issues:

| Issue | Description | Fix Applied |
|---|---|---|
| **Duplicate records** | 3% of customers appeared twice due to a simulated system glitch | Deduplicated on `customer_id`, keeping first occurrence |
| **Missing values** | ~5% of customers had no `last_login_date` on record | Flagged via a `login_data_missing` boolean column instead of guessing fake values |
| **Inconsistent categorical data** | Plan names appeared as `Premium`, `PREM`, `Premiun`, `premium `, etc. | Standardized via string cleaning + mapping dictionary |

## 🛠️ Tech Stack

- **Python (pandas, Faker)** — synthetic data generation & cleaning
- **SQL (SQLite)** — data storage and analytical querying
- **Streamlit** — interactive, filterable web dashboard

## 🔍 Key Insights

1. **Support ticket volume is the strongest churn predictor.** Customers with 0–2 tickets 
   churn at ~45–48%, but churn jumps to **76–83%** once a customer files 3+ tickets — 
   suggesting frustration is a leading indicator, actionable via proactive outreach triggers.
2. **Missing engagement data is itself a risk signal.** Customers with no recorded login 
   activity churned at **64.4%**, vs. 49.6% for customers with known activity — meaning 
   "unknown" should be treated as high-risk, not neutral.
3. **Tenure doesn't behave as expected.** Churned customers had *longer* average tenure 
   (403 days) than retained customers (349 days), challenging the assumption that only new 
   customers are flight risks.

## 📂 Project Structure

## ▶️ How to Run This Project

```bash
# 1. Clone this repo and navigate into it
git clone <your-repo-url>
cd churn-detective-project

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install pandas faker streamlit

# 4. Run the pipeline in order
python3 generate_data.py
python3 clean_data.py
python3 load_to_sql.py
python3 analysis_queries.py

# 5. Launch the dashboard
streamlit run dashboard.py
```

## 📊 Dashboard Preview

*(Add a screenshot of your dashboard here after uploading to GitHub)*

---

**Note:** This project uses synthetically generated mock data (via Python's Faker library) 
built to demonstrate an end-to-end analytics workflow and data-cleaning methodology — the 
churn rate (~50%) is intentionally simplified for demonstration and is not representative 
of real-world subscription benchmarks.