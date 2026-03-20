"""
Validation Checks - VECTORIZED version (no iterrows)
4a. PERSON_ID Reliability
4b. COUNSEL_CATEGORY by County (DUI records)
4c. Charge-Level vs. Case-Level Metrics (DUI)
4d. UNIQUE_CORRELATION_ID - Case Linkage
4e. Temporal Consistency
"""

import zipfile, pandas as pd, numpy as np, json, os
from collections import Counter, defaultdict
from config import ZIP_PATH, OUTPUT_DIR, MISSING_VALS

print("Starting vectorized validation checks...", flush=True)

# We'll do two passes:
# Pass 1: accumulate aggregated stats (groupby operations) - fast
# Pass 2: not needed - all done in pass 1

# Accumulators (all vectorized)
# 4a: PERSON_ID - need per-case set of PIDs
#     We'll build a dataframe of (case_id, person_id, county) and do groupby
person_id_chunks = []   # list of (UNIQUE_CORRELATION_ID, PERSON_ID, COUNTY_DESCRIPTION) frames

# 4b: COUNSEL_CATEGORY by county for DUI
counsel_chunks = []  # list of (COUNTY_DESCRIPTION, COUNSEL_CATEGORY) for DUI rows

# 4c: DUI rows for charge vs case analysis
dui_chunks = []  # list of (UNIQUE_CORRELATION_ID, Disposition) for DUI rows

# 4d: All rows for case linkage
linkage_chunks = []  # list of (UNIQUE_CORRELATION_ID, STATUTE, FCIC_Category, is_dui)

# 4e: Temporal - (year, Disposition, COUNTY_DESCRIPTION)
temporal_chunks = []

CHUNK_SIZE = 200000
total_rows = 0

with zipfile.ZipFile(ZIP_PATH) as z:
    for fname in sorted(z.namelist()):
        print(f"Processing {fname}...", flush=True)
        with z.open(fname) as f:
            for chunk in pd.read_csv(f, chunksize=CHUNK_SIZE, dtype=str, low_memory=False):
                total_rows += len(chunk)

                # Normalize
                for col in ['STATUTE','FCIC_Category','Disposition','COUNTY_DESCRIPTION',
                             'PERSON_ID','MDM_PERSON_ID','UNIQUE_CORRELATION_ID',
                             'COUNSEL_CATEGORY','Race','Sex','DISPOSITION_DATE']:
                    if col in chunk.columns:
                        chunk[col] = chunk[col].fillna('').str.strip()

                # DUI mask (Method B)
                mask_dui = (
                    chunk['STATUTE'].str.startswith('316.193', na=False) &
                    ~chunk['STATUTE'].str.startswith('316.1935', na=False) &
                    ~chunk['STATUTE'].str.startswith('316.1939', na=False)
                )

                # 4a: PERSON_ID per case - collect minimal columns
                pid_frame = chunk[['UNIQUE_CORRELATION_ID','PERSON_ID','COUNTY_DESCRIPTION']].copy()
                pid_frame = pid_frame[pid_frame['UNIQUE_CORRELATION_ID'] != '']
                person_id_chunks.append(pid_frame)

                # 4b: COUNSEL_CATEGORY for DUI
                dui_chunk = chunk[mask_dui][['COUNTY_DESCRIPTION','COUNSEL_CATEGORY']].copy()
                counsel_chunks.append(dui_chunk)

                # 4c: DUI rows for disposition analysis
                dui_disp = chunk[mask_dui][['UNIQUE_CORRELATION_ID','Disposition','COUNTY_DESCRIPTION']].copy()
                dui_chunks.append(dui_disp)

                # 4d: Case linkage - all rows
                link_frame = chunk[['UNIQUE_CORRELATION_ID','STATUTE','FCIC_Category']].copy()
                link_frame['is_dui'] = mask_dui
                link_frame = link_frame[link_frame['UNIQUE_CORRELATION_ID'] != '']
                linkage_chunks.append(link_frame)

                # 4e: Temporal
                try:
                    dates = pd.to_datetime(chunk['DISPOSITION_DATE'], errors='coerce')
                    year_series = dates.dt.year
                    temp_frame = pd.DataFrame({
                        'year': year_series,
                        'Disposition': chunk['Disposition'],
                        'COUNTY_DESCRIPTION': chunk['COUNTY_DESCRIPTION']
                    })
                    temp_frame = temp_frame[temp_frame['year'].notna() &
                                           (temp_frame['year'] >= 1990) &
                                           (temp_frame['year'] <= 2030)]
                    temp_frame['year'] = temp_frame['year'].astype(int)
                    temporal_chunks.append(temp_frame)
                except Exception as e:
                    print(f"  Temporal error: {e}", flush=True)

print(f"\nTotal rows: {total_rows}", flush=True)
print("Concatenating chunks...", flush=True)

# ---- 4a: PERSON_ID Analysis ----
print("\n4a: PERSON_ID Analysis...", flush=True)
pid_df = pd.concat(person_id_chunks, ignore_index=True)
pid_df = pid_df[pid_df['PERSON_ID'] != '']

# Cases with multiple PERSON_IDs
case_pid_nunique = pid_df.groupby('UNIQUE_CORRELATION_ID')['PERSON_ID'].nunique()
total_cases = len(case_pid_nunique)
cases_one_pid = int((case_pid_nunique == 1).sum())
cases_multi_pid = int((case_pid_nunique > 1).sum())
cases_no_pid = int(
    pid_df[pid_df['PERSON_ID'] == '']['UNIQUE_CORRELATION_ID'].nunique()
)

# Cross-county: PIDs appearing in multiple counties
pid_county_nunique = pid_df.groupby('PERSON_ID')['COUNTY_DESCRIPTION'].nunique()
total_pids = len(pid_county_nunique)
pids_multi_county = int((pid_county_nunique > 1).sum())

print(f"  Total cases: {total_cases}", flush=True)
print(f"  Cases with 1 PID: {cases_one_pid}", flush=True)
print(f"  Cases with multiple PIDs: {cases_multi_pid}", flush=True)
print(f"  Unique PIDs: {total_pids}", flush=True)
print(f"  PIDs in 2+ counties: {pids_multi_county}", flush=True)

# Sample of cases with multiple PIDs
multi_pid_cases = case_pid_nunique[case_pid_nunique > 1].head(5).index.tolist()
multi_pid_sample = {}
for cid in multi_pid_cases:
    pids = pid_df[pid_df['UNIQUE_CORRELATION_ID'] == cid]['PERSON_ID'].unique().tolist()
    multi_pid_sample[cid] = pids

del pid_df
print("  4a done.", flush=True)

# ---- 4b: COUNSEL_CATEGORY ----
print("\n4b: COUNSEL_CATEGORY by County (DUI)...", flush=True)
counsel_df = pd.concat(counsel_chunks, ignore_index=True)
counsel_df['is_populated'] = (
    counsel_df['COUNSEL_CATEGORY'].notna() &
    ~counsel_df['COUNSEL_CATEGORY'].isin(MISSING_VALS) &
    (counsel_df['COUNSEL_CATEGORY'] != '')
)
counsel_stats = counsel_df.groupby('COUNTY_DESCRIPTION').agg(
    total=('is_populated', 'count'),
    populated=('is_populated', 'sum')
).reset_index()
counsel_stats['pct'] = (counsel_stats['populated'] / counsel_stats['total'] * 100).round(1)
counsel_stats = counsel_stats.sort_values('total', ascending=False)
counsel_results = counsel_stats.set_index('COUNTY_DESCRIPTION').to_dict('index')
del counsel_df
print("  4b done.", flush=True)

# ---- 4c: Charge vs Case Level ----
print("\n4c: Charge vs Case Level...", flush=True)
dui_df = pd.concat(dui_chunks, ignore_index=True)
total_dui_charges = len(dui_df)
print(f"  Total DUI charges: {total_dui_charges}", flush=True)

# Charge level
charge_level_disp = dui_df['Disposition'].value_counts().to_dict()

# Case level - most serious disposition hierarchy
DISP_HIERARCHY = {
    'Adjudicated Guilty': 1,
    'Adjudication Withheld': 2,
    'Pre-Trial Diversion': 3,
    'Dismissed': 4,
    'Acquitted': 5,
    'Mentally Unable to Stand Trial': 6,
    'Civil/Non Criminal': 7,
    'Acquitted by Reason of Insanity': 8,
    'Bond Estreature': 9,
    'Dismissed Speedy Trial': 10,
    'Transfer to Civil Court': 11,
    'Closed/Non-Florida Case': 12,
    'Adjudged Delinquent': 13,
    'Change of Venue': 14,
    'Decline to Adjudicate': 15,
}
dui_df['disp_rank'] = dui_df['Disposition'].map(DISP_HIERARCHY).fillna(99).astype(int)
# For each case, pick the row with the lowest rank (most serious)
case_disp = dui_df.sort_values('disp_rank').groupby('UNIQUE_CORRELATION_ID').first().reset_index()
total_dui_cases = len(case_disp)
case_level_disp = case_disp['Disposition'].value_counts().to_dict()
print(f"  Total DUI cases: {total_dui_cases}", flush=True)
del dui_df
print("  4c done.", flush=True)

# ---- 4d: Case Linkage ----
print("\n4d: Case Linkage...", flush=True)
link_df = pd.concat(linkage_chunks, ignore_index=True)

# Charges per case distribution
charges_per_case = link_df.groupby('UNIQUE_CORRELATION_ID').size()
charges_per_case_dist = charges_per_case.value_counts().sort_index().to_dict()
avg_charges_all = float(charges_per_case.mean())
median_charges_all = float(charges_per_case.median())

# DUI cases
dui_case_ids = set(link_df[link_df['is_dui']]['UNIQUE_CORRELATION_ID'].unique())
dui_case_charges = charges_per_case[charges_per_case.index.isin(dui_case_ids)]
avg_charges_dui = float(dui_case_charges.mean()) if len(dui_case_charges) > 0 else 0
median_charges_dui = float(dui_case_charges.median()) if len(dui_case_charges) > 0 else 0
dui_case_charge_dist = dui_case_charges.value_counts().sort_index().to_dict()

# Co-occurring charges in DUI cases (non-DUI charges only)
dui_cases_df = link_df[link_df['UNIQUE_CORRELATION_ID'].isin(dui_case_ids)]
non_dui_in_dui_cases = dui_cases_df[~dui_cases_df['is_dui']]
co_charge_counts = non_dui_in_dui_cases.groupby(['STATUTE','FCIC_Category']).size().sort_values(ascending=False)
top15_co_charges = [
    {'statute': s, 'fcic': f, 'count': int(c)}
    for (s, f), c in co_charge_counts.head(15).items()
]

del link_df
print(f"  Total cases: {len(charges_per_case)}", flush=True)
print(f"  DUI cases: {len(dui_case_ids)}", flush=True)
print("  4d done.", flush=True)

# ---- 4e: Temporal Consistency ----
print("\n4e: Temporal Consistency...", flush=True)
temp_df = pd.concat(temporal_chunks, ignore_index=True)

# Disposition categories by year
disp_by_year = temp_df.groupby(['year','Disposition']).size().reset_index(name='count')
disp_by_year_dict = {}
for year, grp in disp_by_year.groupby('year'):
    disp_by_year_dict[int(year)] = grp.set_index('Disposition')['count'].to_dict()

# County year ranges
county_year_range = temp_df.groupby('COUNTY_DESCRIPTION')['year'].agg(['min','max']).to_dict('index')

# Disposition categories that appear/disappear
all_years = sorted(disp_by_year_dict.keys())
disp_first_year = {}
disp_last_year = {}
for year, disps in disp_by_year_dict.items():
    for d in disps:
        if d not in disp_first_year:
            disp_first_year[d] = year
        disp_last_year[d] = max(disp_last_year.get(d, 0), year)

del temp_df
print("  4e done.", flush=True)

# ---- Save Results ----
print("\nSaving results...", flush=True)
results = {
    'person_id': {
        'total_cases': total_cases,
        'cases_with_one_pid': cases_one_pid,
        'cases_with_multiple_pids': cases_multi_pid,
        'pct_cases_with_multiple_pids': round(cases_multi_pid / total_cases * 100, 3) if total_cases > 0 else 0,
        'total_unique_pids': total_pids,
        'pids_multi_county': pids_multi_county,
        'pct_pids_multi_county': round(pids_multi_county / total_pids * 100, 2) if total_pids > 0 else 0,
        'multi_pid_sample': multi_pid_sample,
    },
    'counsel_category': {k: {'total': int(v['total']), 'populated': int(v['populated']), 'pct': float(v['pct'])}
                         for k, v in counsel_results.items()},
    'charge_vs_case': {
        'total_dui_charges': total_dui_charges,
        'total_dui_cases': total_dui_cases,
        'avg_charges_per_dui_case': round(total_dui_charges / total_dui_cases, 3) if total_dui_cases > 0 else 0,
        'charge_level_disp': {k: int(v) for k, v in charge_level_disp.items()},
        'case_level_disp': {k: int(v) for k, v in case_level_disp.items()},
    },
    'case_linkage': {
        'total_cases': int(len(charges_per_case)),
        'avg_charges_all': round(avg_charges_all, 3),
        'median_charges_all': median_charges_all,
        'charges_per_case_dist': {int(k): int(v) for k, v in charges_per_case_dist.items()},
        'dui_cases': len(dui_case_ids),
        'avg_charges_dui': round(avg_charges_dui, 3),
        'median_charges_dui': median_charges_dui,
        'dui_case_charge_dist': {int(k): int(v) for k, v in dui_case_charge_dist.items()},
        'top15_dui_co_charges': top15_co_charges,
    },
    'temporal': {
        'disp_by_year': {str(k): {d: int(c) for d, c in v.items()} for k, v in disp_by_year_dict.items()},
        'county_year_range': {k: {'min': int(v['min']), 'max': int(v['max'])} for k, v in county_year_range.items()},
        'disp_first_year': {k: int(v) for k, v in disp_first_year.items()},
        'disp_last_year': {k: int(v) for k, v in disp_last_year.items()},
    },
}

out_path = os.path.join(OUTPUT_DIR, 'validation_results.json')
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"Saved to {out_path}", flush=True)
print("Done!", flush=True)
