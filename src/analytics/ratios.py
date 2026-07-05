"""
Sprint 2 - Day 08
Financial Ratio Engine
"""


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (%)
    Formula: Net Profit / Sales × 100
    """
    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin (%)
    Formula: Operating Profit / Sales × 100
    """
    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (ROE)

    Formula:
    Net Profit / (Equity Capital + Reserves) × 100
    """
    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return round((net_profit / total_equity) * 100, 2)
def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings
):
    """
    Return on Capital Employed (ROCE)

    Formula:
    EBIT / (Equity + Reserves + Borrowings) × 100
    """

    capital = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital <= 0:
        return None

    return round(
        (ebit / capital) * 100,
        2
    )
def return_on_assets(net_profit, total_assets):
    """
    Return on Assets (ROA)

    Formula:
    Net Profit / Total Assets × 100
    """

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)
def debt_to_equity(
    borrowings,
    equity_capital,
    reserves
):
    """
    Debt to Equity Ratio

    Formula:
    Borrowings / (Equity + Reserves)
    """

    if borrowings == 0:
        return 0

    total_equity = (
        equity_capital
        + reserves
    )

    if total_equity <= 0:
        return None

    return round(
        borrowings / total_equity,
        2
    )
def high_leverage_flag(debt_equity_ratio, broad_sector):
    """
    High Leverage Flag

    Returns True if:
    - D/E > 5
    - Company is NOT in Financials sector
    """

    if (
        debt_equity_ratio is not None
        and debt_equity_ratio > 5
        and broad_sector != "Financials"
    ):
        return True

    return False
def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio (ICR)

    Formula:
    (Operating Profit + Other Income) / Interest
    """

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income)
        / interest,
        2
    )
def icr_label(icr):
    """
    Returns Debt Free label.
    """

    if icr is None:
        return "Debt Free"


    return ""
def icr_warning(icr):
    """
    Returns True if Interest Coverage Ratio is below 1.5
    """

    if icr is None:
        return False

    return icr < 1.5
def asset_turnover(sales, total_assets):
    """
    Asset Turnover

    Formula:
    Sales / Total Assets
    """

    if total_assets == 0:
        return None

    return round(sales / total_assets, 2)
def net_debt(borrowings, investments):
    """
    Net Debt

    Formula:
    Borrowings - Investments
    """
    return borrowings - investments

