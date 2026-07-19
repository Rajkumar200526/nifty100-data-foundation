import pandas as pd

from src.screener.engine import apply_filters


def test_apply_filters():

    df = pd.DataFrame({
        "company_name": ["A", "B"],
        "roe": [20, 10],
        "roce": [18, 9],
        "net_profit_margin_pct": [15, 8],
        "debt_to_equity": [0.5, 2.0],
        "free_cash_flow": [100, -50],
        "asset_turnover": [0.6, 0.4],
        "interest_coverage": [5, 1],
        "sales": [1000, 300]
    })

    config = {
        "roe_min": 15,
        "debt_to_equity_max": 1,
        "free_cash_flow_min": 0,
        "asset_turnover_min": 0.5,
        "interest_coverage_min": 2,
        "sales_min": 500
    }

    result = apply_filters(df, config)

    assert len(result) == 1
    assert result.iloc[0]["company_name"] == "A"