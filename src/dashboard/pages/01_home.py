import streamlit as st
import plotly.express as px
import pandas as pd
from utils.db import run_query
st.set_page_config(layout="wide")

st.title("📊 Nifty 100 Financial Intelligence Dashboard")
st.caption("Interactive Financial Analytics & Company Performance Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.header("Dashboard Filters")

selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5
)


st.write(f"### Financial Year : {selected_year}")

company_list = run_query("""
SELECT company_name
FROM companies
ORDER BY company_name;
""")

selected_company = st.sidebar.selectbox(
    "Select Company",
    options=company_list["company_name"].tolist(),
    index=0,
    key="company_select"
)

st.write(f"### Selected Company : {selected_company}")


company_id = run_query("""
SELECT company_id
FROM companies
WHERE company_name = ?;
""", (selected_company,))

company_id = int(company_id.iloc[0]["company_id"])
st.write("Company ID:", company_id)
# KPI Row
col1, col2, col3 = st.columns(3)

average_roe = run_query("""
SELECT ROUND(roe_percentage, 2) AS avg_roe
FROM companies
WHERE company_id = ?;
""", (company_id,))

with col1:
   st.metric(
    label="📈 Average ROE",
    value=f"{average_roe.iloc[0]['avg_roe']}%"
)

with col2:
    st.metric("Median P/E", "N/A")

average_roce = run_query("""
SELECT ROUND(roce_percentage, 2) AS avg_roce
FROM companies
WHERE company_id = ?;
""", (company_id,))

with col3:
    st.metric(
    label="🏆 Average ROCE",
    value=f"{average_roce.iloc[0]['avg_roce']}%"
)

col4, col5, col6 = st.columns(3)

company_count = run_query("""
SELECT COUNT(*) AS total
FROM companies;
""")


with col4:
    st.metric(
    label="🏢 Total Companies",
    value=int(company_count.iloc[0]["total"])
)

revenue_growth = run_query("""
SELECT ROUND(
    ((curr.sales - prev.sales) * 100.0) / prev.sales,
    2
) AS growth
FROM profitandloss curr
JOIN profitandloss prev
ON curr.company_id = prev.company_id
WHERE curr.company_id = ?
AND curr.year = 2024
AND prev.year = 2023
AND prev.sales > 0;
""", (company_id,))
with col5:
    value = revenue_growth.iloc[0]["growth"]

    st.metric(
    label="📊 Revenue Growth",
    value=f"{value:.2f}%"
)

debt_free = run_query("""
SELECT borrowings
FROM balancesheet
WHERE company_id = ?
AND year = 2024;
""", (company_id,))

with col6:

    borrowings = debt_free.iloc[0]["borrowings"]

    if borrowings == 0:
        debt_status = "Debt Free"
    else:
        debt_status = "Has Debt"

    st.metric(
    label="💰 Debt Status",
    value=debt_status
)
    

left_col, right_col = st.columns([2, 1])
st.info(
    f"""
📊 **Company Summary**

**Company:** {selected_company}

**ROE:** {average_roe.iloc[0]['avg_roe']}%

**ROCE:** {average_roce.iloc[0]['avg_roce']}%

**Revenue Growth:** {revenue_growth.iloc[0]['growth']:.2f}%

**Debt Status:** {debt_status}
"""
)
st.markdown("---")
st.subheader("📈 Revenue Trend")

revenue_df = run_query("""
SELECT
    year,
    sales
FROM profitandloss
WHERE company_id = ?
ORDER BY year;
""", (company_id,))
fig = px.line(
    revenue_df,
    x="year",
    y="sales",
    markers=True,
    title=f"{selected_company} Revenue Trend",
    labels={
        "year": "Financial Year",
        "sales": "Sales (₹ Crores)"
    }
)
fig.update_traces(
    hovertemplate="<b>Year:</b> %{x}<br><b>Sales:</b> ₹%{y:,.0f}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)
with left_col:
    st.subheader("Sector Distribution")


# Temporary sample data until official dataset is available
sector_df = run_query("""
SELECT
    broad_sector AS Sector,
    COUNT(*) AS Companies
FROM companies
GROUP BY broad_sector
ORDER BY Companies DESC;
""")

selected_sector = run_query("""
SELECT broad_sector
FROM companies
WHERE company_id = ?;
""", (company_id,))
selected_sector = selected_sector.iloc[0]["broad_sector"]

st.write("Selected Sector:", selected_sector)

fig = px.pie(
    sector_df,
    names="Sector",
    values="Companies",
    hole=0.5,
    title=f"Sector Distribution ({selected_company})"
)
fig.update_traces(
    pull=[
        0.15 if sector == selected_sector else 0
        for sector in sector_df["Sector"]
    ]
)

st.plotly_chart(fig, use_container_width=True)
fig.update_layout(
    template="plotly_white",
    xaxis_title="Financial Year",
    yaxis_title="Sales (₹ Crores)",
    hovermode="x unified"
)

st.markdown("---")
with right_col:
    st.subheader("Top 5 Companies by Composite Score")

    ranking_metric = st.selectbox(
        "Rank Companies By",
        ["ROE", "ROCE"]
    )

    if ranking_metric == "ROE":
        order_column = "roe_percentage"
    else:
        order_column = "roce_percentage"

    top5_df = run_query(f"""
    SELECT
    company_name AS Company,
    roe_percentage AS "ROE (%)",
    roce_percentage AS "ROCE (%)"
FROM companies
    ORDER BY {order_column} DESC
    LIMIT 5;
    """)
if ranking_metric == "ROE":
    order_column = "roe_percentage"
else:
    order_column = "roce_percentage"
top5_df.insert(0, "Rank", range(1, len(top5_df) + 1))
top5_df["Company"] = top5_df["Company"].apply(
    lambda x: f"⭐ {x}" if x == selected_company else x
)
if ranking_metric == "ROE":
    top5_df = top5_df[["Rank", "Company", "ROE (%)"]]
else:
    top5_df = top5_df[["Rank", "Company", "ROCE (%)"]]
st.dataframe(
    top5_df,
    use_container_width=True,
    hide_index=True
)
