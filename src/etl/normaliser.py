"""
normaliser.py
Sprint 1 Day 02
"""

import re

def normalize_year(year):

    if year is None:
        return None

    year = str(year).strip()

    if year.replace(".", "", 1).isdigit():
        return int(float(year))

    match = re.search(r'(\d{4})', year)

    if match:
        return int(match.group(1))

    raise ValueError(f"Invalid year: {year}")


def normalize_ticker(ticker):

    if ticker is None:
        return None

    ticker = str(ticker).strip().upper()

    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(".BO", "")

    return ticker