"""
Sprint 2 – Day 11
Cash Flow KPIs
"""


def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow (FCF)

    Formula:
    CFO + CFI
    """

    return operating_activity + investing_activity
def cfo_quality_score(cfo, pat):
    """
    CFO Quality Score
    """

    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1.0:
        return "High Quality"

    elif ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"
def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity
    """

    if sales == 0:
        return None

    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        label = "Asset Light"
    elif intensity <= 8:
        label = "Moderate"
    else:
        label = "Capital Intensive"

    return round(intensity, 2), label
def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion Rate
    """

    if operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)
def capital_allocation_pattern(cfo, cfi, cff):
    """
    Capital Allocation Pattern Classifier
    """

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    patterns = {
        ("+","-","-"): "Reinvestor",
        ("+","+","-"): "Liquidating Assets",
        ("-","+","+"): "Distress Signal",
        ("-","-","+"): "Growth Funded by Debt",
        ("+","+","+"): "Cash Accumulator",
        ("-","-","-"): "Pre-Revenue",
        ("+","-","+"): "Mixed"
    }

    return patterns.get(signs, "Other")