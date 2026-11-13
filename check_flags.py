import pandas as pd

df = pd.read_csv("data_raw/DE1_0_2010_Beneficiary_Summary_File_Sample_1.csv", usecols=["SP_DIABETES", "SP_CHF", "SP_COPD"])
for col in df.columns:
    print(col, dict(df[col].value_counts(dropna=False)))
