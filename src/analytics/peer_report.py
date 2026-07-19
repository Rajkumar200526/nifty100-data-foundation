"""
Sprint 3 - Day 20
Peer Comparison Excel Report
"""

import pandas as pd


def export_peer_report(df, filename):
    """
    Export Peer Comparison Report
    """

    # Sort companies by ROE percentile (highest first)
    df = df.sort_values(
        by="roe_percentile",
        ascending=False
    )

    # Export to Excel
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(
            writer,
            sheet_name="Peer Comparison",
            index=False

            )

    print(f"Peer Comparison Report Generated: {filename}")