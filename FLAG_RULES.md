# Flag Rules — Healthcare Coding Explorer

Each rule compares a beneficiary's year with their previous year and adds points.
Score = sum of triggered rules, max 100. Flags are patterns worth a second look,
not findings of incorrect coding. Data: CMS DE-SynPUF Sample 1 (synthetic only).

## The rules in one sentence each
- R1 (30 pts): A person's diagnosis codes jump sharply in one year — up at least 15 codes and at least 50% over the year before.
- R2 (25 pts): At least 3 chronic conditions recorded for a person in one year are missing the next year.
- R3 (25 pts): A person gains at least 3 new chronic conditions in one year with no hospital (inpatient) payment that year.
- R4 (20 pts): The same condition category (first 3 digits of the main diagnosis) is billed by at least 6 different doctors for one person in one year.

## First tuned run (2026-11-13)
- Person-years compared (2009 vs 2008, 2010 vs 2009): 227,292
- R1 triggered: 18,727 | R2 triggered: 41,895 | R3 triggered: 10,051 | R4 triggered: 3,747
- Total flagged (score > 0): 67,909 (30% of compared person-years); highest score: 80

## Tuning notes
- First pass used R2 >= 1 vanished (124,775 = 55% — too noisy: in this synthetic data the chronic flags flicker; only 45% of person-years have zero vanish) and R3 >= 2 (23,323).
- Thresholds were re-set from the actual distributions: R2 >= 3 vanished, R3 >= 3 jump. R1 and R4 were already selective and were left unchanged.
- Spot check: the top flag (score 80) was hand-verified against the person's features — diagnosis jump, the 3 named vanished conditions, and the +3 chronic rise with no inpatient payment all match the raw rows.
