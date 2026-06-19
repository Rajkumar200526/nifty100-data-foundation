from src.etl.normaliser import normalize_ticker


def test_uppercase():
    assert normalize_ticker("tcs") == "TCS"


def test_remove_ns():
    assert normalize_ticker("infy.ns") == "INFY"


def test_remove_bo():
    assert normalize_ticker("reliance.bo") == "RELIANCE"


def test_strip_spaces():
    assert normalize_ticker(" hdfcbank ") == "HDFCBANK"
def test_upper():
    assert normalize_ticker("SBIN") == "SBIN"

def test_lower():
    assert normalize_ticker("sbin") == "SBIN"

def test_ns_suffix():
    assert normalize_ticker("sbin.ns") == "SBIN"

def test_bo_suffix():
    assert normalize_ticker("sbin.bo") == "SBIN"

def test_none():
    assert normalize_ticker(None) is None
def test_tcs():
    assert normalize_ticker("tcs") == "TCS"

def test_infy():
    assert normalize_ticker("infy") == "INFY"

def test_reliance():
    assert normalize_ticker("reliance") == "RELIANCE"

def test_hdfcbank():
    assert normalize_ticker("hdfcbank") == "HDFCBANK"

def test_icicibank():
    assert normalize_ticker("icicibank") == "ICICIBANK"

def test_sbin():
    assert normalize_ticker("sbin") == "SBIN"

def test_axisbank():
    assert normalize_ticker("axisbank") == "AXISBANK"

def test_wipro():
    assert normalize_ticker("wipro") == "WIPRO"

def test_bajaj():
    assert normalize_ticker("bajajfin") == "BAJAJFIN"

def test_ltim():
    assert normalize_ticker("ltim") == "LTIM"