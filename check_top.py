import pandas as pd

pid = "B654944EA6DCC9F5"
CHRONIC = ["SP_ALZHDMTA", "SP_CHF", "SP_CHRNKIDN", "SP_CNCR", "SP_COPD",
           "SP_DEPRESSN", "SP_DIABETES", "SP_ISCHMCHT", "SP_OSTEOPRS",
           "SP_RA_OA", "SP_STRKETIA"]
f = pd.read_csv("data_processed/bene_year_features.csv")
rows = f[f["DESYNPUF_ID"] == pid].sort_values("year")
print(rows[["year", "chronic_count", "diag_codes", "claims", "has_inpatient"] + CHRONIC].to_string(index=False))
print()
fl = pd.read_csv("outputs/flag_list.csv")
top = fl[fl["DESYNPUF_ID"] == pid]
print(top[["year", "score", "rules", "reason"]].to_string(index=False))
