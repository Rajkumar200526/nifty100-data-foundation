import pandas as pd

# Read Excel files
companies = pd.read_excel("data/raw/companies.xlsx")
profit = pd.read_excel("data/raw/profitandloss.xlsx")
balance = pd.read_excel("data/raw/balancesheet.xlsx")
cashflow = pd.read_excel("data/raw/cashflow.xlsx")

# Merge Profit & Loss with Balance Sheet
df = profit.merge(
    balance,
    on=["company_id", "year"],
    how="inner"
)

# Merge Cash Flow
df = df.merge(
    cashflow,
    on=["company_id", "year"],
    how="inner"
)

# Merge Company Master
df = df.merge(
    companies,
    on="company_id",
    how="left"
)

# Reorder important columns
columns = [
    "company_id",
    "company_name",
    "year",
    "sales",
    "operating_profit",
    "net_profit",
    "equity_capital",
    "reserves",
    "borrowings",
    "total_assets",
    "other_income",
    "interest",
    "operating_activity",
    "investing_activity"
]

df = df[columns]

# Save CSV
df.to_csv(
    "data/processed/financial_data.csv",
    index=False
)

print("Financial data created successfully.")
print("Rows:", len(df))
print(df.head())