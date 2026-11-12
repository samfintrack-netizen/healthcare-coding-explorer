# Data Notes — Healthcare Coding Explorer

## Source
CMS DE-SynPUF (Data Entrepreneurs' Synthetic Public Use Files), Sample 1 only, years 2008-2010.
Fully synthetic, fictional Medicare beneficiaries. Synthetic data only — never real claims, never employer data.
Raw files live locally in data_raw/ and are NOT in this repo (.gitignore).

## Files loaded
- Beneficiary Summary 2008 / 2009 / 2010 — 1 ZIP each, ~14 MB CSV each, 32 columns
- Carrier Claims 2008-2010, files 1A and 1B — ~1.2 GB CSV each, 142 columns
- Reference: DE 1.0 Codebook (CMS)

## Checkpoint answers (from my own load, 2026-11-12)
- Beneficiaries: 116,352 in 2008; 114,538 in 2009; 112,754 in 2010
- In each Beneficiary file, rows = distinct DESYNPUF_IDs — one row per person per year
- Beneficiary count falls slightly each year (attrition / death)
- Carrier claims: 4,741,335 rows total (1A: 2,370,667; 1B: 2,370,668)
- Distinct beneficiaries with at least one carrier claim: 98,626
- Claim years present (from CLM_FROM_DT): 2008, 2009, 2010

## Linking key
DESYNPUF_ID — beneficiary code present in every file; links Beneficiary Summary to Carrier Claims.
It is synthetic and carries no real patient information.

## Beneficiary Summary — key columns (32)
- DESYNPUF_ID: beneficiary code (linking key)
- BENE_BIRTH_DT, BENE_DEATH_DT: birth / death dates
- BENE_SEX_IDENT_CD, BENE_RACE_CD, BENE_ESRD_IND: demographics / ESRD indicator
- SP_STATE_CODE, BENE_COUNTY_CD: state / county
- BENE_HI_CVRAGE_TOT_MONS, BENE_SMI_CVRAGE_TOT_MONS, BENE_HMO_CVRAGE_TOT_MONS, PLAN_CVRG_MOS_NUM: coverage months
- 11 chronic-condition flags for that year: SP_ALZHDMTA, SP_CHF, SP_CHRNKIDN, SP_CNCR, SP_COPD, SP_DEPRESSN, SP_DIABETES, SP_ISCHMCHT, SP_OSTEOPRS, SP_RA_OA, SP_STRKETIA
- Yearly money totals by setting (IP = inpatient, OP = outpatient, CAR = carrier): MEDREIMB_* (Medicare paid), BENRES_* (beneficiary responsibility), PPPYMT_* (primary payer paid)
- One row = one beneficiary in one year

## Carrier Claims — key columns (142)
- DESYNPUF_ID: beneficiary code (linking key); CLM_ID: claim ID
- CLM_FROM_DT, CLM_THRU_DT: claim start / end dates (YYYYMMDD)
- ICD9_DGNS_CD_1..8: up to 8 ICD-9 diagnosis codes on the claim
- Wide line format: suffixes _1.._13 are the claim's service lines, flattened into columns
  - HCPCS_CD_1..13: procedure code per line
  - PRF_PHYSN_NPI_1..13: performing physician per line
  - LINE_NCH_PMT_AMT_1..13: Medicare payment per line
  - LINE_ICD9_DGNS_CD_1..13: diagnosis code per line
  - Plus per-line deductible, coinsurance, allowed charge columns
- One row = one physician/supplier (carrier) claim, not one line item

## Notes / limits
- Diagnosis codes are ICD-9 (the coding system in use in 2008-2010), not ICD-10
- Flags built on this data are patterns worth a second look, not findings of incorrect coding
