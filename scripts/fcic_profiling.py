"""
Query 4: FCIC top-15 charge type profiling
For each of the top 15 FCIC categories (by record count, 2023-2025):
  - Total cases
  - County coverage breadth (# counties with >100 cases)
  - Disposition distribution: Guilty%, AW%, Dismissed%, Diversion%
  - AW > 10%? (flag)
  - COUNSEL_CATEGORY completeness %
  - Distinct STATUTE values (1-3 = clean, 10+ = messy)
"""
import zipfile, pandas as pd, numpy as np, json, os
from config import ZIP_PATH, OUTPUT_DIR, CHUNK_SIZE
DATE_MIN = pd.Timestamp('2023-01-01')
DATE_MAX = pd.Timestamp('2025-12-31')

print("Loading data (2023-2025, all dispositions)...", flush=True)

chunks = []
with zipfile.ZipFile(ZIP_PATH) as z:
    for fname in sorted(z.namelist()):
        print(f"  {fname}", flush=True)
        with z.open(fname) as f:
            for chunk in pd.read_csv(
                f, chunksize=CHUNK_SIZE, dtype=str, low_memory=False,
                usecols=['UNIQUE_CORRELATION_ID', 'FCIC_Category', 'STATUTE',
                         'Disposition', 'COUNTY_DESCRIPTION', 'DISPOSITION_DATE',
                         'COUNSEL_CATEGORY']
            ):
                for col in chunk.columns:
                    chunk[col] = chunk[col].fillna('').str.strip()

                chunk['_date'] = pd.to_datetime(chunk['DISPOSITION_DATE'], errors='coerce')
                mask_date = (chunk['_date'] >= DATE_MIN) & (chunk['_date'] <= DATE_MAX)
                filtered = chunk[mask_date].copy()
                if len(filtered) > 0:
                    chunks.append(filtered)

df = pd.concat(chunks, ignore_index=True)
print(f"\nTotal rows 2023-2025: {len(df)}", flush=True)

# Deduplicate to case level for case counts
# Rename for consistency
df = df.rename(columns={'FCIC_Category': 'FCIC_CATEGORY'})
df_cases = df.drop_duplicates('UNIQUE_CORRELATION_ID').copy()
print(f"Unique cases: {len(df_cases)}", flush=True)

# Get top 15 FCIC categories by case count
top15 = (df_cases['FCIC_CATEGORY']
         .replace('', 'BLANK/MISSING')
         .value_counts()
         .head(16)
         .index.tolist())
# Remove blank if it's in there and add back at end
if 'BLANK/MISSING' in top15:
    top15.remove('BLANK/MISSING')
    top15 = top15[:15]
else:
    top15 = top15[:15]

print(f"\nTop 15 FCIC categories: {top15}", flush=True)

# Disposition normalization
def normalize_disp(val):
    v = str(val).lower().strip()
    if 'adjudicated guilty' in v or v == 'guilty':
        return 'Guilty'
    if 'adjudication withheld' in v or 'withheld' in v:
        return 'AW'
    if 'dismissed' in v or 'nolle' in v or 'nol pros' in v:
        return 'Dismissed'
    if 'diversion' in v or 'pretrial' in v or 'deferred' in v or 'drug court' in v:
        return 'Diversion'
    if 'not guilty' in v or 'acquitted' in v:
        return 'Not Guilty'
    if 'pending' in v or 'open' in v:
        return 'Pending'
    return 'Other'

df_cases['disp_norm'] = df_cases['Disposition'].apply(normalize_disp)

results = []
for fcic in top15:
    sub = df_cases[df_cases['FCIC_CATEGORY'] == fcic].copy()
    # Also check blank-mapped
    if fcic == 'BLANK/MISSING':
        sub = df_cases[df_cases['FCIC_CATEGORY'] == ''].copy()

    n_cases = len(sub)
    if n_cases == 0:
        continue

    # County coverage: # counties with >100 cases
    county_counts = sub['COUNTY_DESCRIPTION'].value_counts()
    n_counties_100 = int((county_counts > 100).sum())

    # Disposition distribution
    disp_counts = sub['disp_norm'].value_counts()
    total_disp = disp_counts.sum()
    guilty_pct = round(disp_counts.get('Guilty', 0) / total_disp * 100, 1)
    aw_pct = round(disp_counts.get('AW', 0) / total_disp * 100, 1)
    dismissed_pct = round(disp_counts.get('Dismissed', 0) / total_disp * 100, 1)
    diversion_pct = round(disp_counts.get('Diversion', 0) / total_disp * 100, 1)
    aw_flag = aw_pct > 10

    # COUNSEL_CATEGORY completeness
    counsel_filled = (sub['COUNSEL_CATEGORY'] != '').sum()
    counsel_pct = round(counsel_filled / n_cases * 100, 1)

    # Distinct STATUTE values
    # Use the raw df (not deduped) to get all statute values for this FCIC
    sub_raw = df[df['FCIC_CATEGORY'] == fcic]
    distinct_statutes = sub_raw['STATUTE'].replace('', pd.NA).dropna().nunique()

    # Statute complexity rating
    if distinct_statutes <= 3:
        statute_rating = 'Clean'
    elif distinct_statutes <= 9:
        statute_rating = 'Moderate'
    else:
        statute_rating = 'Messy'

    # Top 5 statutes for context
    top_statutes = sub_raw['STATUTE'].value_counts().head(5).index.tolist()

    result = {
        'fcic_category': fcic,
        'n_cases': n_cases,
        'n_counties_100': n_counties_100,
        'guilty_pct': guilty_pct,
        'aw_pct': aw_pct,
        'dismissed_pct': dismissed_pct,
        'diversion_pct': diversion_pct,
        'aw_flag': aw_flag,
        'counsel_completeness_pct': counsel_pct,
        'distinct_statutes': distinct_statutes,
        'statute_rating': statute_rating,
        'top_statutes': top_statutes
    }
    results.append(result)

    print(f"\n{fcic}:")
    print(f"  Cases: {n_cases:,} | Counties(>100): {n_counties_100}")
    print(f"  Guilty: {guilty_pct}% | AW: {aw_pct}% {'[FLAG]' if aw_flag else ''} | Dismissed: {dismissed_pct}% | Diversion: {diversion_pct}%")
    print(f"  Counsel completeness: {counsel_pct}%")
    print(f"  Distinct statutes: {distinct_statutes} ({statute_rating}) | Top: {top_statutes[:3]}")

with open(os.path.join(OUTPUT_DIR, 'fcic_profiling_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("\nSaved to fcic_profiling_results.json")
print("Done!")
