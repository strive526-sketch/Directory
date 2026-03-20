"""
Validation Checks:
4a. PERSON_ID Reliability
4b. COUNSEL_CATEGORY by County (DUI records)
4c. Charge-Level vs. Case-Level Metrics (DUI)
4d. UNIQUE_CORRELATION_ID - Case Linkage
4e. Temporal Consistency
"""

import zipfile, io, pandas as pd, numpy as np, json
from collections import Counter, defaultdict

ZIP_PATH = "/home/ubuntu/cjdt/CjdtClerkCase.zip"
MISSING_VALS = {"Not Available", "N/A", "NA", "", "nan", "None", "NULL", "null"}

print("Starting validation checks...", flush=True)

# We'll accumulate data for all checks in one pass
# For PERSON_ID: track per-case (UNIQUE_CORRELATION_ID) the set of PERSON_IDs
# For COUNSEL_CATEGORY: track by county for DUI records
# For charge vs case: need full DUI subset
# For linkage: charges per case distribution
# For temporal: disposition categories by year

# Data structures
# 4a: PERSON_ID per case
case_person_ids = defaultdict(set)  # UNIQUE_CORRELATION_ID -> set of PERSON_IDs
case_counties = {}  # UNIQUE_CORRELATION_ID -> county (first seen)
person_demo = {}  # PERSON_ID -> (Race, Sex) for consistency check

# 4b: COUNSEL_CATEGORY by county for DUI
dui_counsel_county = defaultdict(lambda: {'total': 0, 'populated': 0})

# 4c: DUI charges for case-level analysis
# We need to store all DUI rows - that's ~350k rows, manageable
dui_rows_list = []

# 4d: Charges per case (all records)
case_charge_counts = Counter()  # UNIQUE_CORRELATION_ID -> count (we'll do this differently)
# Actually track case_id -> charge list for co-occurrence
case_charges = defaultdict(list)  # case_id -> list of (STATUTE, FCIC_Category)
dui_case_ids = set()  # cases that have at least one DUI charge

# 4e: Disposition by year
disp_by_year = defaultdict(Counter)  # year -> disposition -> count
county_first_year = {}  # county -> first year seen
county_last_year = {}   # county -> last year seen

CHUNK_SIZE = 200000
total_rows = 0

with zipfile.ZipFile(ZIP_PATH) as z:
    for fname in sorted(z.namelist()):
        print(f"Processing {fname}...", flush=True)
        with z.open(fname) as f:
            for chunk in pd.read_csv(f, chunksize=CHUNK_SIZE, dtype=str, low_memory=False):
                total_rows += len(chunk)

                # Normalize key fields
                chunk['STATUTE'] = chunk['STATUTE'].fillna('').str.strip()
                chunk['FCIC_Category'] = chunk['FCIC_Category'].fillna('').str.strip()
                chunk['Disposition'] = chunk['Disposition'].fillna('').str.strip()
                chunk['COUNTY_DESCRIPTION'] = chunk['COUNTY_DESCRIPTION'].fillna('').str.strip()
                chunk['PERSON_ID'] = chunk['PERSON_ID'].fillna('').str.strip()
                chunk['MDM_PERSON_ID'] = chunk['MDM_PERSON_ID'].fillna('').str.strip()
                chunk['UNIQUE_CORRELATION_ID'] = chunk['UNIQUE_CORRELATION_ID'].fillna('').str.strip()
                chunk['COUNSEL_CATEGORY'] = chunk['COUNSEL_CATEGORY'].fillna('').str.strip()
                chunk['Race'] = chunk['Race'].fillna('').str.strip()
                chunk['Sex'] = chunk['Sex'].fillna('').str.strip()

                # DUI mask (Method B)
                mask_b_raw = chunk['STATUTE'].str.startswith('316.193', na=False)
                mask_b_exclude = (
                    chunk['STATUTE'].str.startswith('316.1935', na=False) |
                    chunk['STATUTE'].str.startswith('316.1939', na=False)
                )
                mask_dui = mask_b_raw & ~mask_b_exclude

                # 4a: PERSON_ID per case
                for _, row in chunk[['UNIQUE_CORRELATION_ID', 'PERSON_ID', 'MDM_PERSON_ID',
                                      'COUNTY_DESCRIPTION', 'Race', 'Sex']].iterrows():
                    cid = row['UNIQUE_CORRELATION_ID']
                    pid = row['PERSON_ID']
                    if cid and pid:
                        case_person_ids[cid].add(pid)
                        if cid not in case_counties:
                            case_counties[cid] = row['COUNTY_DESCRIPTION']
                    # Track demographics for consistency check
                    if pid and pid not in person_demo:
                        person_demo[pid] = (row['Race'], row['Sex'])

                # 4b: COUNSEL_CATEGORY for DUI
                dui_chunk = chunk[mask_dui]
                for _, row in dui_chunk[['COUNTY_DESCRIPTION', 'COUNSEL_CATEGORY']].iterrows():
                    county = row['COUNTY_DESCRIPTION']
                    cc = row['COUNSEL_CATEGORY']
                    dui_counsel_county[county]['total'] += 1
                    if cc and cc not in MISSING_VALS:
                        dui_counsel_county[county]['populated'] += 1

                # 4c: Collect DUI rows for case-level analysis
                if len(dui_rows_list) < 500000:  # cap at 500k to avoid OOM
                    dui_rows_list.append(dui_chunk[['UNIQUE_CORRELATION_ID', 'Disposition',
                                                     'STATUTE', 'FCIC_Category',
                                                     'COUNTY_DESCRIPTION']].copy())

                # 4d: Case linkage - track charges per case and co-occurring charges
                for _, row in chunk[['UNIQUE_CORRELATION_ID', 'STATUTE', 'FCIC_Category']].iterrows():
                    cid = row['UNIQUE_CORRELATION_ID']
                    if cid:
                        case_charges[cid].append((row['STATUTE'], row['FCIC_Category']))
                        if mask_dui.loc[row.name] if row.name in mask_dui.index else False:
                            dui_case_ids.add(cid)

                # 4e: Temporal consistency
                try:
                    dates = pd.to_datetime(chunk['DISPOSITION_DATE'], errors='coerce')
                    chunk['_year'] = dates.dt.year
                    for _, row in chunk[['_year', 'Disposition', 'COUNTY_DESCRIPTION']].dropna(subset=['_year']).iterrows():
                        year = int(row['_year'])
                        disp = row['Disposition']
                        county = row['COUNTY_DESCRIPTION']
                        if 1990 <= year <= 2030:
                            disp_by_year[year][disp] += 1
                            if county:
                                if county not in county_first_year or year < county_first_year[county]:
                                    county_first_year[county] = year
                                if county not in county_last_year or year > county_last_year[county]:
                                    county_last_year[county] = year
                except Exception as e:
                    print(f"  Temporal error: {e}", flush=True)

print(f"\nTotal rows: {total_rows}", flush=True)

# ---- 4a: PERSON_ID Analysis ----
print("\n4a: PERSON_ID Analysis...", flush=True)
cases_with_multiple_pids = 0
cases_with_one_pid = 0
cases_with_no_pid = 0
total_cases = len(case_person_ids)

for cid, pids in case_person_ids.items():
    if len(pids) == 0:
        cases_with_no_pid += 1
    elif len(pids) == 1:
        cases_with_one_pid += 1
    else:
        cases_with_multiple_pids += 1

# Cross-county check: find PERSON_IDs that appear in multiple counties
pid_counties = defaultdict(set)
for cid, county in case_counties.items():
    for pid in case_person_ids[cid]:
        if pid:
            pid_counties[pid].add(county)

pids_multi_county = sum(1 for pid, counties in pid_counties.items() if len(counties) > 1)
total_pids = len(pid_counties)

# Demo consistency check: sample 10k PERSON_IDs that appear multiple times
# Check if Race/Sex changes
# We stored only first occurrence in person_demo - need to check for conflicts
# Let's do a second pass on a sample
print(f"  Total cases: {total_cases}", flush=True)
print(f"  Cases with 1 PERSON_ID: {cases_with_one_pid}", flush=True)
print(f"  Cases with multiple PERSON_IDs: {cases_with_multiple_pids}", flush=True)
print(f"  Cases with no PERSON_ID: {cases_with_no_pid}", flush=True)
print(f"  Total unique PERSON_IDs: {total_pids}", flush=True)
print(f"  PERSON_IDs appearing in 2+ counties: {pids_multi_county}", flush=True)

# ---- 4b: COUNSEL_CATEGORY ----
print("\n4b: COUNSEL_CATEGORY by County (DUI)...", flush=True)
counsel_results = {}
for county, stats in sorted(dui_counsel_county.items(), key=lambda x: -x[1]['total']):
    total = stats['total']
    populated = stats['populated']
    pct = populated / total * 100 if total > 0 else 0
    counsel_results[county] = {'total': total, 'populated': populated, 'pct': round(pct, 1)}

# ---- 4c: Charge vs Case Level ----
print("\n4c: Charge vs Case Level...", flush=True)
dui_df = pd.concat(dui_rows_list, ignore_index=True) if dui_rows_list else pd.DataFrame()
print(f"  DUI rows collected: {len(dui_df)}", flush=True)

charge_level_disp = {}
case_level_disp = {}

if len(dui_df) > 0:
    # Charge level
    charge_level_disp = dui_df['Disposition'].value_counts().to_dict()

    # Case level - use most serious disposition hierarchy
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

    def get_rank(disp):
        return DISP_HIERARCHY.get(disp, 99)

    # Group by case, pick most serious disposition
    case_disp = dui_df.groupby('UNIQUE_CORRELATION_ID')['Disposition'].apply(
        lambda x: min(x, key=get_rank)
    ).reset_index()
    case_disp.columns = ['UNIQUE_CORRELATION_ID', 'case_disposition']
    case_level_disp = case_disp['case_disposition'].value_counts().to_dict()

    total_dui_charges = len(dui_df)
    total_dui_cases = len(case_disp)
    print(f"  Total DUI charges: {total_dui_charges}", flush=True)
    print(f"  Total DUI cases: {total_dui_cases}", flush=True)

# ---- 4d: Case Linkage ----
print("\n4d: Case Linkage...", flush=True)
# Distribution of charges per case
charges_per_case = Counter(len(v) for v in case_charges.values())
print(f"  Total cases: {len(case_charges)}", flush=True)

# For DUI cases: co-occurring charges
dui_co_charges = Counter()
dui_case_charge_counts = Counter()
for cid in dui_case_ids:
    charges = case_charges.get(cid, [])
    dui_case_charge_counts[len(charges)] += 1
    for statute, fcic in charges:
        # Only count non-DUI co-charges
        if not statute.startswith('316.193') or statute.startswith('316.1935') or statute.startswith('316.1939'):
            dui_co_charges[(statute, fcic)] += 1

print(f"  DUI cases: {len(dui_case_ids)}", flush=True)
print(f"  Top 15 co-charges in DUI cases:", flush=True)
for (statute, fcic), count in dui_co_charges.most_common(15):
    print(f"    {statute} ({fcic}): {count}", flush=True)

# ---- 4e: Temporal Consistency ----
print("\n4e: Temporal Consistency...", flush=True)
# Get all disposition categories that appear in each year
all_disps = set()
for year_disps in disp_by_year.values():
    all_disps.update(year_disps.keys())

# County reporting years
county_year_range = {
    county: (county_first_year.get(county), county_last_year.get(county))
    for county in set(list(county_first_year.keys()) + list(county_last_year.keys()))
}

# ---- Save Results ----
print("\nSaving results...", flush=True)

# Convert case_person_ids to summary stats (too large to save fully)
pid_mismatch_sample = [(cid, list(pids)) for cid, pids in list(case_person_ids.items())[:5]
                        if len(pids) > 1]

results = {
    # 4a
    'person_id': {
        'total_cases': total_cases,
        'cases_with_one_pid': cases_with_one_pid,
        'cases_with_multiple_pids': cases_with_multiple_pids,
        'cases_with_no_pid': cases_with_no_pid,
        'pct_cases_with_multiple_pids': round(cases_with_multiple_pids / total_cases * 100, 3) if total_cases > 0 else 0,
        'total_unique_pids': total_pids,
        'pids_multi_county': pids_multi_county,
        'pct_pids_multi_county': round(pids_multi_county / total_pids * 100, 2) if total_pids > 0 else 0,
        'pid_mismatch_sample': pid_mismatch_sample,
    },
    # 4b
    'counsel_category': counsel_results,
    # 4c
    'charge_vs_case': {
        'total_dui_charges': len(dui_df) if len(dui_df) > 0 else 0,
        'total_dui_cases': total_dui_cases if len(dui_df) > 0 else 0,
        'charge_level_disp': charge_level_disp,
        'case_level_disp': case_level_disp,
    },
    # 4d
    'case_linkage': {
        'total_cases': len(case_charges),
        'charges_per_case_dist': dict(sorted(charges_per_case.items())),
        'dui_cases': len(dui_case_ids),
        'dui_case_charge_counts': dict(sorted(dui_case_charge_counts.items())),
        'top15_dui_co_charges': [
            {'statute': s, 'fcic': f, 'count': c}
            for (s, f), c in dui_co_charges.most_common(15)
        ],
    },
    # 4e
    'temporal': {
        'disp_by_year': {str(y): dict(d) for y, d in sorted(disp_by_year.items())},
        'county_year_range': {k: list(v) for k, v in sorted(county_year_range.items())},
    },
}

with open('/home/ubuntu/cjdt/validation_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("Saved to /home/ubuntu/cjdt/validation_results.json", flush=True)
print("Done!", flush=True)
