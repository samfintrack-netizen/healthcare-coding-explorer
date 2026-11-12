import pandas as pd

for year in (2008, 2009, 2010):
    df = pd.read_csv(f"data_raw/DE1_0_{year}_Beneficiary_Summary_File_Sample_1.csv")
    print(year, "rows:", f"{len(df):,}", "| distinct beneficiaries:", f"{df['DESYNPUF_ID'].nunique():,}", "| columns:", len(df.columns))
