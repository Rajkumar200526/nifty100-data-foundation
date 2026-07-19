import streamlit as st
import pandas as pd
from io import BytesIO
st.title("📄 Reports Dashboard")
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
report_types = [
    "Company Profile",
    "Financial Ratios",
    "Peer Comparison",
    "Financial Trends",
    "Sector Analysis",
    "Capital Allocation",
    "Complete Report"
]

selected_report = st.selectbox(
    "Select Report Type",
    report_types
)
st.success(
    f"Company: {selected_company} | Report: {selected_report}"
)
report_df = pd.DataFrame({
    "Metric": [
        "Revenue",
        "Net Profit",
        "ROE",
        "ROCE",
        "Debt to Equity"
    ],
    "Value": [
        118000,
        24000,
        18.2,
        22.5,
        0.18
    ]
})
st.markdown("---")
st.subheader("Export Options")
csv_data = report_df.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="financial_report.csv",
    mime="text/csv"
)
excel_buffer = BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    report_df.to_excel(writer, index=False, sheet_name="Report")

excel_buffer.seek(0)

st.download_button(
    label="📊 Download Excel",
    data=excel_buffer,
    file_name="financial_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
st.button("📄 Generate PDF Report", disabled=True)

st.caption("PDF export will be enabled after integrating the reporting engine.")
if st.button("🚀 Generate Report"):
    st.success(
        f"{selected_report} generated successfully for {selected_company}."
    )