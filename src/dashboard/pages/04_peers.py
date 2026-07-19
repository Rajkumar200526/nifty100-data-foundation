import streamlit as st
import pandas as pd
import plotly.graph_objects as go
st.title("👥 Peer Comparison")
st.markdown("---")
peer_groups = [
    "Information Technology",
    "Financial Services",
    "Energy",
    "FMCG",
    "Healthcare",
    "Industrials",
    "Telecommunication",
    "Automobile",
    "Metals",
    "Pharmaceuticals",
    "Others"
]

selected_group = st.selectbox(
    "Select Peer Group",
    peer_groups
)
st.success(f"Selected Peer Group: {selected_group}")
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
st.markdown("---")
st.subheader("Radar Chart")

metrics = [
    "ROE",
    "ROCE",
    "Net Margin",
    "OPM",
    "FCF",
    "Revenue CAGR",
    "PAT CAGR",
    "Asset Turnover"
]
company_values = [
    18,
    22,
    20,
    25,
    19,
    16,
    17,
    21
]

peer_average = [
    15,
    19,
    17,
    22,
    15,
    14,
    15,
    18
]
fig = go.Figure()
fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=metrics,
        fill="toself",
        name=selected_company
    )
)
fig.add_trace(
    go.Scatterpolar(
        r=peer_average,
        theta=metrics,
        fill="toself",
        name="Peer Average"
    )
)
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 30]
        )
    ),
    showlegend=True,
    height=600
)
st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("Peer Comparison Metrics")
comparison_df = pd.DataFrame({
    "Metric": [
        "ROE",
        "ROCE",
        "Net Profit Margin",
        "Operating Profit Margin",
        "Revenue CAGR",
        "PAT CAGR",
        "Debt to Equity",
        "Free Cash Flow"
    ],
    selected_company: [
        18.2,
        22.5,
        19.3,
        24.1,
        15.8,
        16.2,
        0.18,
        12500
    ],
    "Peer Average": [
        15.6,
        19.7,
        17.4,
        21.8,
        13.9,
        14.6,
        0.42,
        9800
    ]
})
st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)