import streamlit as st
import pandas as pd
import sqlite3

# --- Page setup ---
st.set_page_config(page_title="Churn Detective Dashboard", layout="wide", page_icon="🕵️")

# --- Connect to our database ---
conn = sqlite3.connect("churn.db")
df = pd.read_sql("SELECT * FROM customers", conn)
conn.close()

# ===========================================================
# SIDEBAR — Filters (this is our interactive control panel)
# ===========================================================
st.sidebar.header("🔍 Filter the Data")
plan_options = ["All Plans"] + sorted(df["plan_type"].unique().tolist())
selected_plan = st.sidebar.selectbox("Plan Type", plan_options)

ticket_range = st.sidebar.slider(
    "Support Tickets Filed",
    min_value=int(df["support_tickets"].min()),
    max_value=int(df["support_tickets"].max()),
    value=(int(df["support_tickets"].min()), int(df["support_tickets"].max()))
)

# Apply filters to create a working copy of the data
filtered_df = df.copy()
if selected_plan != "All Plans":
    filtered_df = filtered_df[filtered_df["plan_type"] == selected_plan]
filtered_df = filtered_df[
    (filtered_df["support_tickets"] >= ticket_range[0]) &
    (filtered_df["support_tickets"] <= ticket_range[1])
]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(filtered_df):,}** of {len(df):,} total customers")

# ===========================================================
# HEADER
# ===========================================================
st.title("🕵️ Subscription Churn Detective Dashboard")
st.markdown(
    "**Business question:** Which customers are leaving, and what early-warning signals predict it? "
    "Built on a cleaned, real-world-messy mock dataset (2,000 customers)."
)
st.divider()

# ===========================================================
# TOP-LINE KPI CARDS (based on filtered data)
# ===========================================================
total_customers = len(filtered_df)
churned_count = filtered_df["churned"].sum()
churn_rate = round(100 * churned_count / total_customers, 1) if total_customers > 0 else 0
revenue_at_risk = round(filtered_df[filtered_df["churned"] == 1]["monthly_charge"].sum(), 2)
avg_tenure_churned = round(filtered_df[filtered_df["churned"] == 1]["tenure_days"].mean(), 0) if churned_count > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churn Rate", f"{churn_rate}%")
col3.metric("Monthly Revenue at Risk", f"${revenue_at_risk:,.2f}")
col4.metric("Avg. Tenure (Churned)", f"{int(avg_tenure_churned)} days")

st.divider()

# ===========================================================
# TABS — organizes the dashboard into clear sections
# ===========================================================
tab1, tab2, tab3 = st.tabs(["📊 Key Drivers", "💡 Insights Summary", "🗂️ Raw Data Explorer"])

# -----------------------------------------------------------
# TAB 1: Key Drivers (charts)
# -----------------------------------------------------------
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Churn Rate by Plan Type")
        plan_summary = filtered_df.groupby("plan_type").agg(
            total=("customer_id", "count"), churned=("churned", "sum")
        ).reset_index()
        plan_summary["churn_rate_pct"] = round(100 * plan_summary["churned"] / plan_summary["total"], 1)
        st.bar_chart(plan_summary.set_index("plan_type")["churn_rate_pct"], color="#FF4B4B")

    with c2:
        st.subheader("Churn Rate: Login Data Known vs. Missing")
        login_summary = filtered_df.groupby("login_data_missing").agg(
            total=("customer_id", "count"), churned=("churned", "sum")
        ).reset_index()
        login_summary["churn_rate_pct"] = round(100 * login_summary["churned"] / login_summary["total"], 1)
        login_summary["login_data_missing"] = login_summary["login_data_missing"].map(
            {0: "Login Known", 1: "Login Missing"}
        )
        st.bar_chart(login_summary.set_index("login_data_missing")["churn_rate_pct"], color="#FFA500")

    st.subheader("Churn Rate by Support Ticket Volume")
    st.caption("⚠️ Key finding: churn risk jumps sharply once a customer files 3+ tickets")
    ticket_summary = filtered_df.groupby("support_tickets").agg(
        total=("customer_id", "count"), churned=("churned", "sum")
    ).reset_index()
    ticket_summary["churn_rate_pct"] = round(100 * ticket_summary["churned"] / ticket_summary["total"], 1)
    st.bar_chart(ticket_summary.set_index("support_tickets")["churn_rate_pct"], color="#D62728")

# -----------------------------------------------------------
# TAB 2: Insights Summary (plain-English callouts)
# -----------------------------------------------------------
with tab2:
    st.subheader("What This Data Is Telling Us")

    st.error(
        "**🚨 Support friction is the #1 warning sign.** "
        "Customers with 0–2 support tickets churn at ~45–48%, but customers with **3+ tickets "
        "churn at 76–83%.** Recommendation: trigger a proactive retention outreach the moment a "
        "customer files their 3rd ticket."
    )

    st.warning(
        "**⚠️ Missing activity data is itself a risk signal.** "
        "Customers with no recorded login activity churn at **64.4%**, versus 49.6% for customers "
        "with known activity. 'We don't have data on them' should be treated as a red flag, not a "
        "neutral unknown."
    )

    st.info(
        "**📌 Tenure doesn't behave as expected.** "
        "Churned customers actually had a *longer* average tenure (403 days) than retained customers "
        "(349 days) — pushing back on the assumption that only brand-new customers are flight risks."
    )

# -----------------------------------------------------------
# TAB 3: Raw Data Explorer
# -----------------------------------------------------------
with tab3:
    st.subheader("Explore the Cleaned Dataset")
    st.dataframe(filtered_df, use_container_width=True, height=500)
    st.caption(f"Displaying {len(filtered_df):,} rows based on your sidebar filters.")