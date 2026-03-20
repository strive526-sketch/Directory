"""
Full statewide jail sentence distribution + CTS analysis
Filters: DUI (316.193%), Guilty/AW, 2023-2025, SENTENCE_CONFINEMENT = 'County Jail'
Minimum threshold: ≥50 jail cases per county
Sentinel detection: flag counties where CTS has 999/9999 values in >10% of records
"""
import zipfile, pandas as pd, numpy as np, json, os
from config import ZIP_PATH, OUTPUT_DIR, CHUNK_SIZE
TARGET_DISPS = {'Adjudicated Guilty', 'Adjudication Withheld'}
DATE_MIN = pd.Timestamp('2023-01-01')
DATE_MAX = pd.Timestamp('2025-12-31')
SENTINEL_VALUES = {999, 9999, 99999, 999999}
MIN_JAIL_CASES = 50

print("Loading DUI data (2023-2025)...", flush=True)

chunks = []
with zipfile.ZipFile(ZIP_PATH) as z:
    for fname in sorted(z.namelist()):
        print(f"  {fname}", flush=True)
        with z.open(fname) as f:
            for chunk in pd.read_csv(
                f, chunksize=CHUNK_SIZE, dtype=str, low_memory=False,
                usecols=['UNIQUE_CORRELATION_ID', 'STATUTE', 'Disposition',
                         'COUNTY_DESCRIPTION', 'DISPOSITION_DATE',
                         'SENTENCE_CONFINEMENT', 'MAXIMUM_TERM_DURATION_DAYS',
                         'CREDIT_TIME_SERVED']
            ):
                for col in chunk.columns:
                    chunk[col] = chunk[col].fillna('').str.strip()

                mask_dui = (
                    chunk['STATUTE'].str.startswith('316.193', na=False) &
                    ~chunk['STATUTE'].str.startswith('316.1935', na=False) &
                    ~chunk['STATUTE'].str.startswith('316.1939', na=False)
                )
                mask_disp = chunk['Disposition'].isin(TARGET_DISPS)
                chunk['_date'] = pd.to_datetime(chunk['DISPOSITION_DATE'], errors='coerce')
                mask_date = (chunk['_date'] >= DATE_MIN) & (chunk['_date'] <= DATE_MAX)

                filtered = chunk[mask_dui & mask_disp & mask_date].copy()
                if len(filtered) > 0:
                    chunks.append(filtered)

df = pd.concat(chunks, ignore_index=True)
print(f"\nTotal DUI rows: {len(df)}", flush=True)

# Convert numerics
for col in ['MAXIMUM_TERM_DURATION_DAYS', 'CREDIT_TIME_SERVED']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Deduplicate to case level
df_cases = df.drop_duplicates('UNIQUE_CORRELATION_ID').copy()
print(f"Unique DUI cases: {len(df_cases)}", flush=True)

# Filter to county jail only
def is_county_jail(val):
    v = str(val).lower().strip()
    return 'county jail' in v

df_jail = df_cases[df_cases['SENTENCE_CONFINEMENT'].apply(is_county_jail)].copy()
print(f"County jail cases: {len(df_jail)}", flush=True)

# Get all counties with ≥50 jail cases
county_counts = df_jail['COUNTY_DESCRIPTION'].value_counts()
eligible_counties = county_counts[county_counts >= MIN_JAIL_CASES].index.tolist()
print(f"\nCounties with ≥{MIN_JAIL_CASES} jail cases: {len(eligible_counties)}", flush=True)
print(eligible_counties)

results = []

for county in eligible_counties:
    sub = df_jail[df_jail['COUNTY_DESCRIPTION'] == county].copy()
    n = len(sub)

    term = sub['MAXIMUM_TERM_DURATION_DAYS']
    cts = sub['CREDIT_TIME_SERVED']

    # --- Sentinel detection ---
    cts_numeric = cts.dropna()
    sentinel_count = cts_numeric.isin(SENTINEL_VALUES).sum()
    sentinel_pct = round(sentinel_count / n * 100, 1) if n > 0 else 0
    has_sentinel = sentinel_pct > 10.0

    term_numeric = term.dropna()
    term_sentinel_count = term_numeric.isin(SENTINEL_VALUES).sum()
    term_sentinel_pct = round(term_sentinel_count / n * 100, 1) if n > 0 else 0

    # --- Median max term (exclude sentinels) ---
    term_clean = term[~term.isin(SENTINEL_VALUES)]
    term_median = float(term_clean.median()) if len(term_clean.dropna()) > 0 else None

    # --- % 1-2 days ---
    pct_1_2 = round((term_clean.dropna() <= 2).sum() / n * 100, 1)

    # --- % 3-30 days ---
    pct_3_30 = round(((term_clean.dropna() >= 3) & (term_clean.dropna() <= 30)).sum() / n * 100, 1)

    # --- % 31-90 days ---
    pct_31_90 = round(((term_clean.dropna() >= 31) & (term_clean.dropna() <= 90)).sum() / n * 100, 1)

    # --- % 91+ days ---
    pct_91_plus = round((term_clean.dropna() > 90).sum() / n * 100, 1)

    # --- CTS >= Max Term ---
    cts_clean = cts[~cts.isin(SENTINEL_VALUES)]
    both = sub[['MAXIMUM_TERM_DURATION_DAYS', 'CREDIT_TIME_SERVED']].copy()
    both = both[~both['MAXIMUM_TERM_DURATION_DAYS'].isin(SENTINEL_VALUES)]
    both = both[~both['CREDIT_TIME_SERVED'].isin(SENTINEL_VALUES)]
    both = both.dropna()

    if len(both) > 0:
        covers = (both['CREDIT_TIME_SERVED'] >= both['MAXIMUM_TERM_DURATION_DAYS']).sum()
        cts_covers_pct = round(covers / len(both) * 100, 1)
    else:
        cts_covers_pct = None

    # --- Classification ---
    if has_sentinel:
        # Use sentence length only for sentinel-flagged counties
        if term_median is not None:
            if term_median <= 2:
                classification = 'BOOKING ARTIFACT*'
            elif term_median > 7:
                classification = 'REAL JAIL*'
            else:
                classification = 'MIXED*'
        else:
            classification = 'UNKNOWN*'
    else:
        if term_median is not None and cts_covers_pct is not None:
            if term_median <= 2 and cts_covers_pct >= 70:
                classification = 'BOOKING ARTIFACT'
            elif term_median > 7 and cts_covers_pct < 50:
                classification = 'REAL JAIL'
            else:
                classification = 'MIXED'
        elif term_median is not None:
            if term_median <= 2:
                classification = 'BOOKING ARTIFACT'
            elif term_median > 7:
                classification = 'REAL JAIL'
            else:
                classification = 'MIXED'
        else:
            classification = 'UNKNOWN'

    results.append({
        'county': county,
        'jail_n': n,
        'term_median': term_median,
        'pct_1_2': pct_1_2,
        'pct_3_30': pct_3_30,
        'pct_31_90': pct_31_90,
        'pct_91_plus': pct_91_plus,
        'cts_covers_pct': cts_covers_pct,
        'sentinel_flag': has_sentinel,
        'sentinel_pct': sentinel_pct,
        'classification': classification
    })
    print(f"  {county}: n={n}, median={term_median}d, 1-2d={pct_1_2}%, CTS>={cts_covers_pct}%, sentinel={sentinel_pct}% => {classification}")

# Sort: BOOKING ARTIFACT first, then REAL JAIL, then MIXED, then UNKNOWN; within group by jail_n desc
order = {'BOOKING ARTIFACT': 0, 'BOOKING ARTIFACT*': 0,
         'REAL JAIL': 1, 'REAL JAIL*': 1,
         'MIXED': 2, 'MIXED*': 2,
         'UNKNOWN': 3, 'UNKNOWN*': 3}
results.sort(key=lambda r: (order.get(r['classification'], 9), -r['jail_n']))

with open(os.path.join(OUTPUT_DIR, 'statewide_jail_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nSaved {len(results)} counties to statewide_jail_results.json")
print("Done!")
