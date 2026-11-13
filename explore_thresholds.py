import pandas as pd

CHRONIC = ["SP_ALZHDMTA", "SP_CHF", "SP_CHRNKIDN", "SP_CNCR", "SP_COPD",
           "SP_DEPRESSN", "SP_DIABETES", "SP_ISCHMCHT", "SP_OSTEOPRS",
           "SP_RA_OA", "SP_STRKETIA"]
f = pd.read_csv("data_processed/bene_year_features.csv")
f = f.sort_values(["DESYNPUF_ID", "year"]).reset_index(drop=True)
g = f.groupby("DESYNPUF_ID")
f["prev_year"] = g["year"].shift(1)
f["prev_chronic_count"] = g["chronic_count"].shift(1)
for c in CHRONIC:
    f["prev_" + c] = g[c].shift(1)
f = f[f["year"] - f["prev_year"] == 1].copy()
f["vanished"] = sum(((f["prev_" + c] == 1) & (f[c] == 0)).astype(int) for c in CHRONIC)
f["jump"] = f["chronic_count"] - f["prev_chronic_count"]

print("How many conditions vanished (per person-year):")
print(f["vanished"].value_counts().sort_index().to_string())
print()
for k in (1, 2, 3):
    print(f"R2 at >={k} vanished:", f"{(f['vanished'] >= k).sum():,}")
print()
for k in (2, 3):
    n = ((f["jump"] >= k) & (f["has_inpatient"] == 0)).sum()
    print(f"R3 at jump >={k}, no inpatient:", f"{n:,}")
