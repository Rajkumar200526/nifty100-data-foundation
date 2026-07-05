from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover,
)
def test_debt_to_equity():
    assert debt_to_equity(500, 300, 700) == 0.5


def test_debt_free():
    assert debt_to_equity(0, 300, 700) == 0


def test_negative_equity():
    assert debt_to_equity(100, -200, 100) is None


def test_high_leverage_flag():
    assert high_leverage_flag(6.2, "Information Technology") is True


def test_interest_coverage():
    assert interest_coverage_ratio(500, 100, 200) == 3.0


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_net_debt():
    assert net_debt(1000, 300) == 700


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0