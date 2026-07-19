import streamlit as st
import pandas as pd
import plotly.express as px
st.title("🏭 Sector Performance Dashboard")
st.markdown("---")
sectors = [
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

selected_sector = st.selectbox(
    "Select Sector",
    sectors
)
st.success(f"Selected Sector: {selected_sector}")
sector_df = pd.DataFrame({
    "Sector": [
        "IT",
        "Financial",
        "Energy",
        "FMCG",
        "Healthcare",
        "Industrials"
    ],
    "Average ROE": [
        21.5,
        18.2,
        16.8,
        19.1,
        17.3,
        15.6
    ]
})
st.markdown("---")
st.subheader("Sector-wise Average ROE")
fig = px.bar(
    sector_df,
    x="Sector",
    y="Average ROE",
    text="Average ROE",
    title="Average ROE by Sector"
)
st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("Sector KPIs")
best_sector = sector_df.loc[sector_df["Average ROE"].idxmax()]
lowest_sector = sector_df.loc[sector_df["Average ROE"].idxmin()]
total_sectors = len(sector_df)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🏆 Best Sector",
        best_sector["Sector"],
        f'{best_sector["Average ROE"]:.1f}%'
    )

with col2:
    st.metric(
        "📉 Lowest Sector",
        lowest_sector["Sector"],
        f'{lowest_sector["Average ROE"]:.1f}%'
    )

with col3:
    st.metric(
        "📊 Total Sectors",
        total_sectors
    )
st.markdown("---")
st.subheader("Sector Ranking")

ranking_df = sector_df.sort_values(
    by="Average ROE",
    ascending=False
).reset_index(drop=True)

ranking_df.index = ranking_df.index + 1
ranking_df.index.name = "Rank"

st.dataframe(
    ranking_df,
    use_container_width=True
)