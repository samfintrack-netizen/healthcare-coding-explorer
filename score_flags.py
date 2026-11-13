import pandas as pd

CHRONIC = ["SP_ALZHDMTA", "SP_CHF", "SP_CHRNKIDN", "SP_CNCR", "SP_COPD",
           "SP_DEPRESSN", "SP_DIABETES", "SP_ISCHMCHT", "SP_OSTEOPRS",
           "SP_RA_OA", "SP_STRKETIA"]
NAMES = {"SP_ALZHDMTA": "Alzheimer's", "SP_CHF": "heart failure",
         "SP_CHRNKIDN": "chronic kidney disease", "SP_CNCR": "cancer",
         "SP_COPD": "COPD", "SP_DEPRESSN": "depression", "SP_DIABETES": "diabetes",
         "SP_ISCHMCHT": "ischemic heart disease", "SP_OSTEOPRS": "osteoporosis",
         "SP_RA_OA": "arthritis", "SP_STRKETIA": "stroke/TIA"}

f = pd.read_csv("data_processed/bene_year_features.csv")
f = f.sort_values(["DESYNPUF_ID", "year"]).reset_index(drop=True)
g = f.groupby("DESYNPUF_ID")
f["prev_year"] = g["year"].shift(1)
f["prev_diag_codes"] = g["diag_codes"].shift(1)
f["prev_chronic_count"] = g["chronic_count"].shift(1)
for c in CHRONIC:
    f["prev_" + c] = g[c].shift(1)
f = f[f["year"] - f["prev_year"] == 1].copy()   # only 2009-vs-2008 and 2010-vs-2009
print("Person-years with a previous year to compare:", f"{len(f):,}")

# --- Rule 4 needs one claims pass: providers per condition category ---
pair_parts = []
for suffix in ("1A", "1B"):
    path = f"data_raw/DE1_0_2008_to_2010_Carrier_Claims_Sample_{suffix}.csv"
    for chunk in pd.read_csv(path, usecols=["DESYNPUF_ID", "CLM_FROM_DT", "ICD9_DGNS_CD_1", "PRF_PHYSN_NPI_1"],
                             chunksize=200_000, dtype=str):
        chunk["year"] = chunk["CLM_FROM_DT"].str[:4].astype(int)
        chunk["cond"] = chunk["ICD9_DGNS_CD_1"].str[:3]
        pair_parts.append(chunk[["DESYNPUF_ID", "year", "cond", "PRF_PHYSN_NPI_1"]].dropna().drop_duplicates())
    print(suffix, "done")
pairs = pd.concat(pair_parts).drop_duplicates()
counts = pairs.groupby(["DESYNPUF_ID", "year", "cond"]).size().reset_index(name="n_providers")
top = counts.loc[counts.groupby(["DESYNPUF_ID", "year"])["n_providers"].idxmax()]
top = top.rename(columns={"cond": "top_condition", "n_providers": "max_providers_one_condition"})
f = f.merge(top, on=["DESYNPUF_ID", "year"], how="left")
f["max_providers_one_condition"] = f["max_providers_one_condition"].fillna(0).astype(int)

# --- The 4 rules ---
f["vanished_count"] = sum(((f["prev_" + c] == 1) & (f[c] == 0)).astype(int) for c in CHRONIC)
f["r1"] = (f["prev_diag_codes"] > 0) & (f["diag_codes"] - f["prev_diag_codes"] >= 15) & (f["diag_codes"] >= 1.5 * f["prev_diag_codes"])
f["r2"] = f["vanished_count"] >= 3
f["r3"] = (f["chronic_count"] - f["prev_chronic_count"] >= 3) & (f["has_inpatient"] == 0)
f["r4"] = f["max_providers_one_condition"] >= 6
f["score"] = 30 * f["r1"] + 25 * f["r2"] + 25 * f["r3"] + 20 * f["r4"]
for r in ("r1", "r2", "r3", "r4"):
    print(r.upper(), "triggered:", f"{f[r].sum():,}")

flagged = f[f["score"] > 0].copy().sort_values("score", ascending=False)
print("Total flagged:", f"{len(flagged):,}")

def explain(row):
    reasons, rules = [], []
    if row["r1"]:
        rules.append("R1"); reasons.append(f"Diagnosis codes jumped from {int(row['prev_diag_codes'])} in {int(row['year'])-1} to {int(row['diag_codes'])} in {int(row['year'])}")
    if row["r2"]:
        gone = [NAMES[c] for c in CHRONIC if row["prev_" + c] == 1 and row[c] == 0]
        rules.append("R2"); reasons.append(f"Chronic condition(s) recorded in {int(row['year'])-1} but missing in {int(row['year'])}: {', '.join(gone)}")
    if row["r3"]:
        rules.append("R3"); reasons.append(f"Chronic conditions rose from {int(row['prev_chronic_count'])} to {int(row['chronic_count'])} with no hospital (inpatient) payment in {int(row['year'])}")
    if row["r4"]:
        rules.append("R4"); reasons.append(f"Condition category {row['top_condition']} was coded by {int(row['max_providers_one_condition'])} different providers in {int(row['year'])}")
    return "; ".join(rules), " | ".join(reasons)

flagged[["rules", "reason"]] = flagged.apply(lambda r: pd.Series(explain(r)), axis=1)
out = flagged[["DESYNPUF_ID", "year", "score", "rules", "reason",
               "diag_codes", "prev_diag_codes", "chronic_count", "prev_chronic_count",
               "vanished_count", "max_providers_one_condition", "top_condition"]]
out.to_csv("outputs/flag_list.csv", index=False)
print("Saved outputs/flag_list.csv:", out.shape)
print(out.head(10)[["DESYNPUF_ID", "year", "score", "rules"]].to_string())
