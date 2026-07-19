import streamlit as st
import pandas as pd
import plotly.express as px
st.title("📈 Financial Trends")
st.markdown("---")
companies = [
    "TCS",
    "Infosys",
    "Reliance",
    "HDFC Bank",
    "ICICI Bank",
    "SBI",
    "Wipro",
    "HCLTech",
    "Tech Mahindra",
    "L&T"
]

selected_company = st.selectbox(
    "Select Company",
    companies
)
metrics = [
    "Revenue",
    "Net Profit",
    "Operating Profit",
    "EPS",
    "ROE",
    "ROCE",
    "Free Cash Flow",
    "Debt to Equity"
]

selected_metric = st.selectbox(
    "Select Financial Metric",
    metrics
)
st.success(
    f"Company: {selected_company} | Metric: {selected_metric}"
)
trend_df = pd.DataFrame({
    "Year": ["2020", "2021", "2022", "2023", "2024"],
    "Value": [85000, 91000, 98000, 107000, 118000]
})
st.markdown("---")
st.subheader(f"{selected_metric} Trend")
fig = px.line(
    trend_df,
    x="Year",
    y="Value",
    markers=True,
    title=f"{selected_company} - {selected_metric}"
)
fig.update_layout(
    xaxis_title="Financial Year",
    yaxis_title=selected_metric,
    height=500
)
st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("Year-over-Year Growth Analysis")

trend_df["YoY Growth (%)"] = (
    trend_df["Value"].pct_change() * 100
).round(2)
latest_value = trend_df["Value"].iloc[-1]
latest_growth = trend_df["YoY Growth (%)"].iloc[-1]
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Latest Value",
        f"{latest_value:,.0f}"
    )

with col2:
    st.metric(
        "YoY Growth",
        f"{latest_growth:.2f}%"
    )
st.dataframe(
    trend_df,
    use_container_width=True,
    hide_index=True
)