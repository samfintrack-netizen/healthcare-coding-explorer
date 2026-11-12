import pandas as pd

total = 0
ids = set()
years = set()
for suffix in ("1A", "1B"):
    path = f"data_raw/DE1_0_2008_to_2010_Carrier_Claims_Sample_{suffix}.csv"
    for chunk in pd.read_csv(path, usecols=["DESYNPUF_ID", "CLM_FROM_DT"], chunksize=200_000, dtype=str):
        total += len(chunk)
        ids.update(chunk["DESYNPUF_ID"].unique())
        years.update(chunk["CLM_FROM_DT"].str[:4].unique())
    print(suffix, "done — running total:", f"{total:,}")
print("TOTAL carrier claim rows:", f"{total:,}")
print("Distinct beneficiaries with a carrier claim:", f"{len(ids):,}")
print("Claim years:", sorted(years))
