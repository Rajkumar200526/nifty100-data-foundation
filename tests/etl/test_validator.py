import pandas as pd
from src.etl.validator import (
    check_pk_uniqueness,
    check_company_year_uniqueness,
    check_fk_integrity
)

from src.etl.validator import (
    check_pk_uniqueness,
    check_company_year_uniqueness
)


def test_pk_unique():

    df = pd.DataFrame({
        "company_id": [1, 2, 3]
    })

    result = check_pk_uniqueness(
        df,
        "company_id"
    )

    assert len(result) == 0


def test_pk_duplicate():

    df = pd.DataFrame({
        "company_id": [1, 1, 2]
    })

    result = check_pk_uniqueness(
        df,
        "company_id"
    )

    assert len(result) == 1


def test_company_year_unique():

    df = pd.DataFrame({
        "company_id": [1, 1],
        "year": [2023, 2024]
    })

    result = check_company_year_uniqueness(df)

    assert len(result) == 0


def test_company_year_duplicate():

    df = pd.DataFrame({
        "company_id": [1, 1],
        "year": [2023, 2023]
    })

    result = check_company_year_uniqueness(df)

    assert len(result) == 1
def test_fk_integrity():

    parent_df = pd.DataFrame({
        "company_id": [1, 2, 3]
    })

    child_df = pd.DataFrame({
        "company_id": [1, 2, 5]
    })

    result = check_fk_integrity(
        child_df,
        parent_df,
        "company_id",
        "company_id"
    )

    assert len(result) == 1
def check_balance_sheet_balance(df):
    pass

def check_opm_crosscheck(df):
    pass

def check_positive_sales(df):
    pass