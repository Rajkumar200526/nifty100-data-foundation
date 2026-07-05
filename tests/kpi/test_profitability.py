from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)
def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20.0
def test_net_profit_margin_zero_sales():
    assert net_profit_margin(200, 0) is None
def test_operating_profit_margin():
    assert operating_profit_margin(250, 1000) == 25.0
def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(250, 0) is None
def test_return_on_equity():
    assert return_on_equity(120, 300, 700) == 12.0
def test_return_on_equity_negative():
    assert return_on_equity(120, -100, 50) is None
def test_return_on_capital_employed():
    assert return_on_capital_employed(
        300,
        500,
        400,
        100
    ) == 30.0
def test_return_on_assets():
    assert return_on_assets(150, 3000) == 5.0