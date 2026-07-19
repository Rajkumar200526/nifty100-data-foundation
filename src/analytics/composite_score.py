"""
Sprint 3 - Day 17
Composite Quality Score
"""

import pandas as pd


def calculate_score(df):
    """
    Calculate Composite Quality Score
    """

    score = (
        df["roe"] * 0.35
        + df["roce"] * 0.25
        + df["net_profit_margin_pct"] * 0.20
        + (100 - df["debt_to_equity"] * 10) * 0.20
    )

    return score.round(2)