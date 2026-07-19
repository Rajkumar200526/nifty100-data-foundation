import streamlit as st
import pandas as pd
import plotly.express as px
st.title("💰 Capital Allocation Dashboard")
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
st.success(f"Selected Company: {selected_company}")
capital_df = pd.DataFrame({
    "Category": [
        "CapEx",
        "Dividends",
        "Debt Repayment",
        "Share Buyback",
        "Cash Reserve"
    ],
    "Amount": [
        3200,
        2500,
        1800,
        1200,
        4300
    ]
})
st.markdown("---")
st.subheader("Capital Allocation Breakdown")
fig = px.pie(
    capital_df,
    names="Category",
    values="Amount",
    title=f"{selected_company} Capital Allocation"
)
fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)
st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("Capital Allocation KPIs")
total_allocation = capital_df["Amount"].sum()

largest = capital_df.loc[
    capital_df["Amount"].idxmax()
]

smallest = capital_df.loc[
    capital_df["Amount"].idxmin()
]

total_categories = len(capital_df)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Allocation",
        f"{total_allocation:,.0f}"
    )

with col2:
    st.metric(
        "🏆 Largest Allocation",
        largest["Category"],
        f'{largest["Amount"]:,.0f}'
    )

with col3:
    st.metric(
        "📉 Smallest Allocation",
        smallest["Category"],
        f'{smallest["Amount"]:,.0f}'
    )

with col4:
    st.metric(
        "📊 Categories",
        total_categories
    )
st.markdown("---")
st.subheader("Capital Allocation Details")

allocation_df = capital_df.sort_values(
    by="Amount",
    ascending=False
).reset_index(drop=True)

st.dataframe(
    allocation_df,
    use_container_width=True,
    hide_index=True
)