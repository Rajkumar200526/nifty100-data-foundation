import streamlit as st
import pandas as pd
import plotly.express as px
st.title("🏢 Company Profile")
st.markdown("---")
company_list = [
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
    company_list
)
st.success(f"You selected: {selected_company}")
company_info = {
    "TCS": {
        "Sector": "Information Technology",
        "Sub Sector": "IT Services",
        "Ticker": "TCS",
        "About": "Tata Consultancy Services is India's largest IT services company."
    },
    "Infosys": {
        "Sector": "Information Technology",
        "Sub Sector": "IT Services",
        "Ticker": "INFY",
        "About": "Infosys provides consulting and digital transformation services."
    },
    "Reliance": {
        "Sector": "Energy",
        "Sub Sector": "Oil & Gas",
        "Ticker": "RELIANCE",
        "About": "Reliance Industries operates in energy, retail, telecom, and digital services."
    }
}
info = company_info.get(
    selected_company,
    {
        "Sector": "N/A",
        "Sub Sector": "N/A",
        "Ticker": "N/A",
        "About": "Information not available."
    }
)
st.markdown("---")

st.subheader("Company Information")

st.write(f"**Company Name:** {selected_company}")
st.write(f"**Sector:** {info['Sector']}")
st.write(f"**Sub Sector:** {info['Sub Sector']}")
st.write(f"**NSE Ticker:** {info['Ticker']}")
st.write(f"**About:** {info['About']}")
st.markdown("---")
st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="ROE",
        value="18.45%"
    )
with col2:
    st.metric(
        label="ROCE",
        value="22.30%"
    )
with col3:
    st.metric(
        label="Net Profit Margin",
        value="21.80%"
    )
col4, col5, col6 = st.columns(3)
with col4:
    st.metric(
        label="Debt to Equity",
        value="0.42"
    )
with col5:
    st.metric(
        label="Revenue CAGR (5Y)",
        value="14.80%"
    )
with col6:
    st.metric(
        label="Free Cash Flow",
        value="₹18,250 Cr"
    )
st.markdown("---")
st.subheader("Revenue & Net Profit (10 Years)")

financial_df = pd.DataFrame({
    "Year": [
        2015, 2016, 2017, 2018, 2019,
        2020, 2021, 2022, 2023, 2024
    ],
    "Revenue": [
        65000, 69000, 72000, 78000, 85000,
        91000, 98000, 108000, 118000, 129000
    ],
    "Net Profit": [
        14500, 15200, 16400, 17100, 18300,
        19100, 20800, 22300, 24100, 25800
    ]
})
chart_df = financial_df.melt(
    id_vars="Year",
    value_vars=["Revenue", "Net Profit"],
    var_name="Metric",
    value_name="Amount"
)
fig = px.bar(
    chart_df,
    x="Year",
    y="Amount",
    color="Metric",
    barmode="group",
    title="Revenue vs Net Profit (10 Years)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("ROE & ROCE Trend (10 Years)")
ratio_df = pd.DataFrame({
    "Year": [
        2015, 2016, 2017, 2018, 2019,
        2020, 2021, 2022, 2023, 2024
    ],
    "ROE": [
        15.2, 16.4, 17.1, 17.8, 18.2,
        18.5, 19.0, 19.4, 20.1, 20.8
    ],
    "ROCE": [
        18.5, 19.1, 20.0, 20.8, 21.3,
        21.8, 22.4, 23.1, 23.8, 24.5
    ]
})
fig = px.line(
    ratio_df,
    x="Year",
    y=["ROE", "ROCE"],
    markers=True,
    title="ROE & ROCE Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("Pros & Cons")
pros_col, cons_col = st.columns(2)
with pros_col:

    st.success("Strengths")

    st.markdown("""
✅ High Return on Equity

✅ Strong Free Cash Flow

✅ Consistent Revenue Growth

✅ Low Debt-to-Equity Ratio

✅ Healthy Operating Margin
""")
with cons_col:

    st.error("Weaknesses")

    st.markdown("""
❌ High Valuation Compared to Peers

❌ Slower Profit Growth in Recent Years

❌ Moderate Capital Expenditure

❌ Revenue Concentration Risk

❌ Competitive Industry Pressure
""")