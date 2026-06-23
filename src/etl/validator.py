"""
validator.py
Sprint 1 Day 03
"""

import pandas as pd
def save_failures(df, output_file):
    df.to_csv(
        output_file,
        index=False
    )


def check_pk_uniqueness(df, column):
    duplicates = df[df.duplicated(column)]
    return duplicates


def check_company_year_uniqueness(df):
    duplicates = df[df.duplicated(
        subset=["company_id", "year"]
    )]
    return duplicates
def check_fk_integrity(
    child_df,
    parent_df,
    child_column,
    parent_column
):

    invalid_rows = child_df[
        ~child_df[child_column].isin(
            parent_df[parent_column]
        )
    ]

    return invalid_rows


def main():
    print("Validator Ready")


if __name__ == "__main__":
    main()