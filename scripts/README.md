# CJDT Analysis Scripts

All scripts operate on the FDLE CJDT Clerk Case bulk download ZIP.
Set `ZIP_PATH` at the top of each script to point to your local copy of `CjdtClerkCase.zip`.

## Direct Download URL (public, no auth required)
https://cjdtpublicstorageprod.blob.core.usgovcloudapi.net/cjdtpubliccontainer/CjdtClerkCase/CjdtClerkCase.zip

## SAO Dataset URL
https://cjdtpublicstorageprod.blob.core.usgovcloudapi.net/cjdtpubliccontainer/CjdtSAOCase/CjdtSAOCase.zip

## Script Index

| Script | Purpose |
|---|---|
| profile_columns.py | Full column-by-column null/completeness profile on all 4M rows |
| dui_analysis.py | DUI subset extraction, Method A vs B comparison, county/temporal distributions |
| validation_checks_v2.py | MDM_PERSON_ID cross-county check, COUNSEL_CATEGORY gaps, charge vs case level |
| fcf_validation.py | Validate FCF published benchmarks vs raw data (Hernando, Pinellas, Duval, statewide) |
| severity_jail_analysis.py | Jail sentence distribution by offense severity (misdemeanor vs felony) |
| top10_jail_analysis.py | Jail duration + credit-time-served analysis for top 10 DUI counties + Marion |
| statewide_jail_analysis.py | Full statewide jail classification (BOOKING ARTIFACT / REAL JAIL / MIXED) for all counties >=50 jail cases |
| feasibility_v2.py | Five net-new feasibility queries: timeline, financials, non-conviction rates, charge stacking, refusal (316.1939) |
| fcic_profiling.py | Top-15 FCIC charge categories: volume, disposition mix, AW rate, statute mapping complexity |
| validation_checks.py | Original (slow) validation script — use v2 instead |
| feasibility_queries.py | Original feasibility script — use v2 instead |

## Requirements
- Python 3.11+
- pandas, numpy (pip install pandas numpy)

## Notes
- The Clerk dataset is ~1.84 GB uncompressed across 5 CSV files
- All scripts use vectorized pandas operations; avoid iterrows()
- DISPOSITION column is mixed-case in the raw CSV: use "Disposition" not "DISPOSITION"
- DUI filter: STATUTE.startswith("316.193") excluding .1935 and .1939
