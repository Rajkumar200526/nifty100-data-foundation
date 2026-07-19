import streamlit as st
import pandas as pd
st.title("📊 Stock Screener")
st.markdown("---")
st.sidebar.header("Screener Filters")
roe_min = st.sidebar.slider(
    "Minimum ROE (%)",
    min_value=0,
    max_value=50,
    value=15
)
de_ratio_max = st.sidebar.slider(
    "Maximum Debt-to-Equity",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1
)
fcf_min = st.sidebar.number_input(
    "Minimum Free Cash Flow (₹ Cr)",
    min_value=0,
    value=0,
    step=100
)
revenue_cagr_min = st.sidebar.slider(
    "Minimum Revenue CAGR (5Y) (%)",
    min_value=-20,
    max_value=50,
    value=10
)
pat_cagr_min = st.sidebar.slider(
    "Minimum PAT CAGR (5Y) (%)",
    min_value=-20,
    max_value=50,
    value=10
)
opm_min = st.sidebar.slider(
    "Minimum Operating Profit Margin (%)",
    min_value=0,
    max_value=60,
    value=15
)
pe_max = st.sidebar.slider(
    "Maximum P/E Ratio",
    min_value=0,
    max_value=100,
    value=30
)
pb_max = st.sidebar.slider(
    "Maximum P/B Ratio",
    min_value=0.0,
    max_value=20.0,
    value=5.0,
    step=0.1
)
dividend_yield_min = st.sidebar.slider(
    "Minimum Dividend Yield (%)",
    min_value=0.0,
    max_value=15.0,
    value=1.0,
    step=0.1
)
icr_min = st.sidebar.slider(
    "Minimum Interest Coverage Ratio",
    min_value=0,
    max_value=50,
    value=3
)
st.markdown("---")
st.subheader("Screening Presets")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
with col1:
    if st.button("⭐ Quality"):
        st.success("Quality preset selected.")
with col2:
    if st.button("💰 Value"):
        st.success("Value preset selected.")
with col3:
    if st.button("📈 Growth"):
        st.success("Growth preset selected.")
with col4:
    if st.button("💵 Dividend"):
        st.success("Dividend preset selected.")
with col5:
    if st.button("🛡️ Debt-Free"):
        st.success("Debt-Free preset selected.")
with col6:
    if st.button("🔄 Turnaround"):
        st.success("Turnaround preset selected.")
st.markdown("---")
st.subheader("Screening Results")
result_count = 0

st.info(f"Companies Matching Filters: {result_count}")
results_df = pd.DataFrame(
    columns=[
        "Company ID",
        "Company Name",
        "Sector",
        "Composite Score",
        "ROE",
        "ROCE",
        "P/E",
        "P/B",
        "Debt to Equity",
        "FCF"
    ]
)
st.dataframe(
    results_df,
    use_container_width=True,
    hide_index=True
)
csv = results_df.to_csv(index=False)

st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name="screener_results.csv",
    mime="text/csv"
)