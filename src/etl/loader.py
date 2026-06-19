from pathlib import Path
import pandas as pd

from src.etl.normaliser import (
    normalize_year,
    normalize_ticker
)

DATA_DIR = Path("data/raw")


def load_excel(file_path):

    df = pd.read_excel(file_path)

    df["year"] = df["year"].apply(normalize_year)
    df["ticker"] = df["ticker"].apply(normalize_ticker)

    return df


def main():

    file_path = DATA_DIR / "sample_companies.xlsx"

    df = load_excel(file_path)

    print(df)


if __name__ == "__main__":
    main()