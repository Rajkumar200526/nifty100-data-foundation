from src.etl.normaliser import normalize_year


def test_year_string():
    assert normalize_year("2024") == 2024


def test_year_float():
    assert normalize_year(2023.0) == 2023


def test_year_fy():
    assert normalize_year("FY2022") == 2022


def test_year_spaces():
    assert normalize_year(" 2021 ") == 2021
def test_year_int():
    assert normalize_year(2025) == 2025

def test_year_float_string():
    assert normalize_year("2020.0") == 2020

def test_year_fy_format():
    assert normalize_year("FY2019") == 2019

def test_year_with_text():
    assert normalize_year("Year 2018") == 2018

def test_none_year():
    assert normalize_year(None) is None
def test_year_2010():
    assert normalize_year("2010") == 2010

def test_year_2011():
    assert normalize_year("2011") == 2011

def test_year_2012():
    assert normalize_year("2012") == 2012

def test_year_2013():
    assert normalize_year("2013") == 2013

def test_year_2014():
    assert normalize_year("2014") == 2014

def test_year_2015():
    assert normalize_year("2015") == 2015

def test_year_2016():
    assert normalize_year("2016") == 2016

def test_year_2017():
    assert normalize_year("2017") == 2017

def test_year_2018():
    assert normalize_year("2018") == 2018

def test_year_2019():
    assert normalize_year("2019") == 2019