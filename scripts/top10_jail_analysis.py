"""
Jail sentence length distribution + CTS analysis for top 10 DUI counties + Marion
Filters: DUI (316.193%), Guilty/AW, 2023-2025, SENTENCE_CONFINEMENT = 'County Jail'
"""
import zipfile, pandas as pd, numpy as np, json, os
from config import ZIP_PATH, OUTPUT_DIR, CHUNK_SIZE
TARGET_DISPS = {'Adjudicated Guilty', 'Adjudication Withheld'}
DATE_MIN = pd.Timestamp('2023-01-01')
DATE_MAX = pd.Timestamp('2025-12-31')

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
                         'CREDIT_TIME_SERVED', 'SENTENCE_PROBATION_DURATION_DAYS']
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
for col in ['MAXIMUM_TERM_DURATION_DAYS', 'CREDIT_TIME_SERVED', 'SENTENCE_PROBATION_DURATION_DAYS']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Deduplicate to case level
df_cases = df.drop_duplicates('UNIQUE_CORRELATION_ID').copy()
print(f"Unique DUI cases: {len(df_cases)}", flush=True)

# Confinement classification
def classify_conf(val):
    v = str(val).lower().strip()
    if 'county jail' in v or (v == 'jail'):
        return 'jail'
    if 'state prison' in v or 'prison facility' in v:
        return 'prison'
    if not val or val in {'', 'not applicable', 'n/a', 'na', 'none', 'null'}:
        return 'none'
    return 'other'

df_cases['conf_type'] = df_cases['SENTENCE_CONFINEMENT'].apply(classify_conf)

# Top 10 counties by DUI case volume
top10 = df_cases['COUNTY_DESCRIPTION'].value_counts().head(10).index.tolist()
print(f"\nTop 10 DUI counties: {top10}", flush=True)

# Ensure Marion is included
target_counties = top10.copy()
if 'Marion' not in target_counties:
    target_counties.append('Marion')
    print("Added Marion to target list")

# Overall jail rate per county (for context)
print("\n--- Overall jail rates for target counties ---")
for county in target_counties:
    sub = df_cases[df_cases['COUNTY_DESCRIPTION'] == county]
    n_total = len(sub)
    n_jail = (sub['conf_type'] == 'jail').sum()
    jail_pct = round(n_jail / n_total * 100, 1) if n_total > 0 else 0
    print(f"  {county}: {n_total} cases, {n_jail} jailed ({jail_pct}%)")

# Jail distribution analysis
def analyze_jail_dist(county_df, county_name):
    jailed = county_df[county_df['conf_type'] == 'jail'].copy()
    n = len(jailed)
    if n == 0:
        return None

    term = jailed['MAXIMUM_TERM_DURATION_DAYS'].dropna()
    cts = jailed['CREDIT_TIME_SERVED'].dropna()

    term_median = float(term.median()) if len(term) > 0 else None

    def bucket(days):
        if pd.isna(days): return 'unknown'
        if days <= 2: return '1-2'
        if days <= 30: return '3-30'
        if days <= 90: return '31-90'
        if days <= 180: return '91-180'
        if days <= 365: return '181-365'
        return '365+'

    jailed['term_bucket'] = jailed['MAXIMUM_TERM_DURATION_DAYS'].apply(bucket)
    bc = jailed['term_bucket'].value_counts()

    pct_1_2 = round(bc.get('1-2', 0) / n * 100, 1)
    pct_3_30 = round(bc.get('3-30', 0) / n * 100, 1)
    pct_31_90 = round(bc.get('31-90', 0) / n * 100, 1)
    pct_91_plus = round((bc.get('91-180', 0) + bc.get('181-365', 0) + bc.get('365+', 0)) / n * 100, 1)

    cts_median = float(cts.median()) if len(cts) > 0 else None

    # % where CTS >= max term
    both = jailed[['MAXIMUM_TERM_DURATION_DAYS', 'CREDIT_TIME_SERVED']].dropna()
    cts_covers_pct = None
    if len(both) > 0:
        covers = (both['CREDIT_TIME_SERVED'] >= both['MAXIMUM_TERM_DURATION_DAYS']).sum()
        cts_covers_pct = round(covers / len(both) * 100, 1)

    # Classification
    # "Booking artifact" = median term <= 2 days AND CTS covers >= 70%
    # "Real jail" = median term > 7 days AND CTS covers < 50%
    # "Mixed" = everything else
    if term_median is not None and cts_covers_pct is not None:
        if term_median <= 2 and cts_covers_pct >= 70:
            pattern = 'BOOKING ARTIFACT'
        elif term_median > 7 and cts_covers_pct < 50:
            pattern = 'REAL JAIL'
        else:
            pattern = 'MIXED'
    else:
        pattern = 'UNKNOWN'

    return {
        'county': county_name,
        'jail_n': n,
        'term_median': term_median,
        'pct_1_2': pct_1_2,
        'pct_3_30': pct_3_30,
        'pct_31_90': pct_31_90,
        'pct_91_plus': pct_91_plus,
        'cts_median': cts_median,
        'cts_covers_pct': cts_covers_pct,
        'pattern': pattern
    }

results = []
print("\n--- Jail distribution analysis ---")
for county in target_counties:
    county_df = df_cases[df_cases['COUNTY_DESCRIPTION'] == county]
    r = analyze_jail_dist(county_df, county)
    if r:
        results.append(r)
        print(f"\n{county}: n={r['jail_n']}, median={r['term_median']}d, "
              f"1-2d={r['pct_1_2']}%, 3-30d={r['pct_3_30']}%, 31-90d={r['pct_31_90']}%, "
              f"91+d={r['pct_91_plus']}%, CTS_med={r['cts_median']}d, "
              f"CTS>={r['cts_covers_pct']}% => {r['pattern']}")
    else:
        print(f"\n{county}: NO JAILED CASES")

with open(os.path.join(OUTPUT_DIR, 'top10_jail_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("\nSaved to top10_jail_results.json")
print("Done!")
