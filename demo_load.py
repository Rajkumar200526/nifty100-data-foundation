import pandas as pd

from src.etl.db_loader import insert_companies

df = pd.DataFrame({
    "company_id": [1, 2],
    "company_name": ["TCS", "Infosys"],
    "ticker": ["TCS", "INFY"]
})

insert_companies(df)