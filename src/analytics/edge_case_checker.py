"""
Sprint 2 Day 13
Edge Case Logger
"""

from pathlib import Path


LOG_FILE = Path("output/ratio_edge_cases.log")


def log_edge_case(company, ratio, expected, calculated, reason):
    """
    Write an anomaly to the log file.
    """

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(
            f"{company} | {ratio} | "
            f"Expected={expected} | "
            f"Calculated={calculated} | "
            f"Reason={reason}\n"
        )
def is_financial_company(broad_sector):
    """
    Returns True for Financial companies.
    """

    return broad_sector == "Financials"
def roe_difference(source, calculated):
    """
    Compare Source ROE with Calculated ROE
    """

    return round(abs(source - calculated), 2)
def roce_difference(source, calculated):
    """
    Compare Source ROCE with Calculated ROCE
    """

    return round(abs(source - calculated), 2)
def categorize_anomaly(difference):
    """
    Categorize ROE/ROCE differences.
    """

    if difference < 1:
        return "OK"

    elif difference <= 5:
        return "Version Difference"

    else:
        return "Formula Discrepancy"