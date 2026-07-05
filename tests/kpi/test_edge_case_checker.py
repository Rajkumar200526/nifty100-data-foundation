from src.analytics.edge_case_checker import (
    is_financial_company,
    roe_difference,
    roce_difference,
    categorize_anomaly,
)
def test_financial_company():
    assert is_financial_company("Financials") is True
def test_non_financial_company():
    assert is_financial_company("IT") is False
def test_roe_difference():
    assert roe_difference(18, 20) == 2
def test_roce_difference():
    assert roce_difference(25, 20) == 5
def test_category_ok():
    assert categorize_anomaly(0.5) == "OK"
def test_category_version_difference():
    assert categorize_anomaly(3) == "Version Difference"
def test_category_formula_discrepancy():
    assert categorize_anomaly(8) == "Formula Discrepancy"
