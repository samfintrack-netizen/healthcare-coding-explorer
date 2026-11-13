import pandas as pd

CHRONIC = ["SP_ALZHDMTA", "SP_CHF", "SP_CHRNKIDN", "SP_CNCR", "SP_COPD",
           "SP_DEPRESSN", "SP_DIABETES", "SP_ISCHMCHT", "SP_OSTEOPRS",
           "SP_RA_OA", "SP_STRKETIA"]
DGNS = [f"ICD9_DGNS_CD_{i}" for i in range(1, 9)]

# --- Part 1: beneficiary summary, one row per person per year ---
bene_parts = []
for year in (2008, 2009, 2010):
    df = pd.read_csv(f"data_raw/DE1_0_{year}_Beneficiary_Summary_File_Sample_1.csv",
                     usecols=["DESYNPUF_ID"] + CHRONIC + ["MEDREIMB_IP", "MEDREIMB_OP", "MEDREIMB_CAR"])
    df["year"] = year
    for c in CHRONIC:
        df[c] = (df[c] == 1).astype(int)   # 1 = has condition, 2 = does not
    df["chronic_count"] = df[CHRONIC].sum(axis=1)
    df["has_inpatient"] = (df["MEDREIMB_IP"] > 0).astype(int)
    bene_parts.append(df)
bene = pd.concat(bene_parts, ignore_index=True)
print("Beneficiary rows:", f"{len(bene):,}")

# --- Part 2: carrier claims, aggregated per person per year (chunked) ---
agg_parts, pair_parts = [], []
for suffix in ("1A", "1B"):
    path = f"data_raw/DE1_0_2008_to_2010_Carrier_Claims_Sample_{suffix}.csv"
    for chunk in pd.read_csv(path, usecols=["DESYNPUF_ID", "CLM_FROM_DT", "PRF_PHYSN_NPI_1"] + DGNS,
                             chunksize=200_000, dtype=str):
        chunk["year"] = chunk["CLM_FROM_DT"].str[:4].astype(int)
        chunk["diag_count"] = chunk[DGNS].notna().sum(axis=1)
        agg_parts.append(chunk.groupby(["DESYNPUF_ID", "year"]).agg(
            claims=("CLM_FROM_DT", "size"), diag_codes=("diag_count", "sum")).reset_index())
        pair_parts.append(chunk[["DESYNPUF_ID", "year", "PRF_PHYSN_NPI_1"]].dropna().drop_duplicates())
    print(suffix, "done")
carrier = pd.concat(agg_parts).groupby(["DESYNPUF_ID", "year"], as_index=False).sum()
pairs = pd.concat(pair_parts).drop_duplicates()
providers = pairs.groupby(["DESYNPUF_ID", "year"]).size().reset_index(name="distinct_providers")
carrier = carrier.merge(providers, on=["DESYNPUF_ID", "year"], how="left")
print("Carrier claims aggregated:", f"{carrier['claims'].sum():,}")

# --- Part 3: join and save ---
features = bene.merge(carrier, on=["DESYNPUF_ID", "year"], how="left")
for c in ("claims", "diag_codes", "distinct_providers"):
    features[c] = features[c].fillna(0).astype(int)
features.to_csv("data_processed/bene_year_features.csv", index=False)
print("Features saved:", features.shape)
print(features.head(10).to_string())
