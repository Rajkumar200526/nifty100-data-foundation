"""
Sprint 3 - Day 18
Peer Comparison Engine
"""

import pandas as pd
def percentile_rank(series):
    """
    Calculate percentile rank.
    """

    return series.rank(pct=True) * 100
def calculate_peer_percentiles(df, metric):
    """
    Calculate percentile ranks for one metric.
    """

    df[f"{metric}_percentile"] = percentile_rank(
        df[metric]
    )

    return df