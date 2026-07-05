from src.analytics.cagr import calculate_cagr


def test_normal_cagr():
    value, flag = calculate_cagr(100, 200, 5)
    assert round(value, 2) == 14.87
    assert flag is None


def test_decline_to_loss():
    value, flag = calculate_cagr(100, -50, 5)
    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_turnaround():
    value, flag = calculate_cagr(-100, 150, 5)
    assert value is None
    assert flag == "TURNAROUND"


def test_both_negative():
    value, flag = calculate_cagr(-100, -50, 5)
    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    value, flag = calculate_cagr(0, 100, 5)
    assert value is None
    assert flag == "ZERO_BASE"


def test_insufficient_years():
    value, flag = calculate_cagr(100, 200, 0)
    assert value is None
    assert flag == "INSUFFICIENT"


def test_three_year_growth():
    value, flag = calculate_cagr(100, 150, 3)
    assert flag is None


def test_five_year_growth():
    value, flag = calculate_cagr(100, 180, 5)
    assert flag is None


def test_ten_year_growth():
    value, flag = calculate_cagr(100, 300, 10)
    assert flag is None


def test_same_value():
    value, flag = calculate_cagr(100, 100, 5)
    assert value == 0.0
    assert flag is None