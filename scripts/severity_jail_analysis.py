"""
Query 1: Severity-controlled sentencing (Misdemeanor vs Felony) for Duval and Hernando
Query 2: Jail sentence length distribution + credit time served for Duval and Hernando
Also: Escambia and Marion for Query 3 prep
"""
import zipfile, pandas as pd, numpy as np, json, os
from config import ZIP_PATH, OUTPUT_DIR, CHUNK_SIZE

TARGET_COUNTIES = {'Hernando', 'Duval', 'Escambia', 'Marion'}
TARGET_DISPS = {'Adjudicated Guilty', 'Adjudication Withheld'}
DATE_MIN = pd.Timestamp('2023-01-01')
DATE_MAX = pd.Timestamp('2025-12-31')

print("Loading data...", flush=True)

chunks = []
with zipfile.ZipFile(ZIP_PATH) as z:
    for fname in sorted(z.namelist()):
        print(f"  {fname}", flush=True)
        with z.open(fname) as f:
            for chunk in pd.read_csv(
                f, chunksize=CHUNK_SIZE, dtype=str, low_memory=False
            ):
                for col in chunk.columns:
                    chunk[col] = chunk[col].fillna('').str.strip()

                # DUI filter
                mask_dui = (
                    chunk['STATUTE'].str.startswith('316.193', na=False) &
                    ~chunk['STATUTE'].str.startswith('316.1935', na=False) &
                    ~chunk['STATUTE'].str.startswith('316.1939', na=False)
                )
                mask_disp = chunk['Disposition'].isin(TARGET_DISPS)
                chunk['_date'] = pd.to_datetime(chunk['DISPOSITION_DATE'], errors='coerce')
                mask_date = (chunk['_date'] >= DATE_MIN) & (chunk['_date'] <= DATE_MAX)
                mask_county = chunk['COUNTY_DESCRIPTION'].isin(TARGET_COUNTIES)

                filtered = chunk[mask_dui & mask_disp & mask_date & mask_county].copy()
                if len(filtered) > 0:
                    chunks.append(filtered)

df = pd.concat(chunks, ignore_index=True)
print(f"\nTotal filtered rows: {len(df)}", flush=True)

# ---- Inspect degree/level field ----
# Find the right field name
degree_candidates = [c for c in df.columns if any(x in c.upper() for x in ['DEGREE', 'LEVEL', 'OFFENSE', 'CLASS', 'SEVERITY'])]
print(f"\nDegree/level candidate columns: {degree_candidates}")
for col in degree_candidates:
    print(f"\n{col} value counts:")
    print(df[col].value_counts().head(15).to_string())

# Convert numeric fields
for col in ['SENTENCE_PROBATION_DURATION_DAYS', 'FINE', 'COURT_COST',
            'MAXIMUM_TERM_DURATION_DAYS', 'CREDIT_TIME_SERVED']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Confinement classification
def classify_confinement(val):
    if not val or val in {'Not Available', 'N/A', 'NA', 'None', 'NULL', 'Not Applicable'}:
        return 'none'
    v = str(val).strip().lower()
    if 'state prison' in v or 'prison facility' in v:
        return 'prison'
    if 'county jail' in v or 'jail' in v:
        return 'jail'
    return 'other'

df['confinement_type'] = df['SENTENCE_CONFINEMENT'].apply(classify_confinement)

# Deduplicate to case level
df_cases = df.drop_duplicates('UNIQUE_CORRELATION_ID').copy()
print(f"\nUnique cases: {len(df_cases)}")

# ---- QUERY 1: Severity-controlled ----
print("\n\n=== QUERY 1: SEVERITY-CONTROLLED SENTENCING ===")

# Determine the degree field to use
# Check OFFENSE_DEGREE_DESCRIPTION or similar
degree_field = None
for candidate in ['OFFENSE_DEGREE_DESCRIPTION', 'OFFENSE_DEGREE', 'CHARGE_DEGREE',
                  'DEGREE_DESCRIPTION', 'DEGREE', 'OFFENSE_LEVEL', 'LEVEL']:
    if candidate in df_cases.columns:
        vals = df_cases[candidate].value_counts()
        if len(vals) > 0 and len(vals) < 20:
            degree_field = candidate
            print(f"Using field: {degree_field}")
            print(vals.to_string())
            break

if degree_field is None:
    # Try to find it from all candidates
    print("Could not auto-detect degree field. Checking all candidates:")
    for col in degree_candidates:
        print(f"\n{col}:")
        print(df_cases[col].value_counts().head(10).to_string())
    # Use first candidate with misdemeanor/felony values
    for col in degree_candidates:
        vals = df_cases[col].str.lower()
        if vals.str.contains('misdemeanor|felony|misd|fel').any():
            degree_field = col
            print(f"\nSelected: {degree_field}")
            break

results_q1 = []
if degree_field:
    # Normalize degree values
    def normalize_degree(val):
        v = str(val).lower()
        if 'felony' in v or v.startswith('f') and len(v) <= 3:
            return 'Felony'
        if 'misdemeanor' in v or 'misd' in v or (v.startswith('m') and len(v) <= 3):
            return 'Misdemeanor'
        return 'Other'

    df_cases['degree_norm'] = df_cases[degree_field].apply(normalize_degree)
    print(f"\nNormalized degree distribution:")
    print(df_cases['degree_norm'].value_counts().to_string())

    for county in ['Duval', 'Hernando']:
        county_df = df_cases[df_cases['COUNTY_DESCRIPTION'] == county]
        for level in ['Misdemeanor', 'Felony']:
            sub = county_df[county_df['degree_norm'] == level]
            n = len(sub)
            if n == 0:
                results_q1.append({'county': county, 'level': level, 'n': 0,
                                   'jail_pct': None, 'prison_pct': None, 'prob_only_pct': None})
                continue
            jail_pct = round((sub['confinement_type'] == 'jail').sum() / n * 100, 1)
            prison_pct = round((sub['confinement_type'] == 'prison').sum() / n * 100, 1)
            prob_only = ((sub['confinement_type'] == 'none') &
                         (sub['SENTENCE_PROBATION_DURATION_DAYS'] > 0)).sum()
            prob_only_pct = round(prob_only / n * 100, 1)
            results_q1.append({
                'county': county, 'level': level, 'n': n,
                'jail_pct': jail_pct, 'prison_pct': prison_pct, 'prob_only_pct': prob_only_pct
            })
            print(f"\n{county} | {level} | n={n} | Jail={jail_pct}% | Prison={prison_pct}% | ProbOnly={prob_only_pct}%")

# ---- QUERY 2: Jail sentence length distribution ----
print("\n\n=== QUERY 2: JAIL SENTENCE LENGTH DISTRIBUTION ===")

results_q2 = []
for county in ['Duval', 'Hernando']:
    county_df = df_cases[df_cases['COUNTY_DESCRIPTION'] == county]
    jailed = county_df[county_df['confinement_type'] == 'jail'].copy()
    n = len(jailed)
    print(f"\n{county}: {n} jailed cases")

    if n == 0:
        results_q2.append({'county': county, 'n': 0})
        continue

    term = jailed['MAXIMUM_TERM_DURATION_DAYS'].dropna()
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
    bucket_counts = jailed['term_bucket'].value_counts()
    bucket_pcts = (bucket_counts / n * 100).round(1)

    print(f"  Median max term: {term_median} days")
    print(f"  Bucket distribution:")
    for b in ['1-2', '3-30', '31-90', '91-180', '181-365', '365+', 'unknown']:
        cnt = bucket_counts.get(b, 0)
        pct = bucket_pcts.get(b, 0.0)
        print(f"    {b}: {cnt} ({pct}%)")

    # Credit time served
    cts_col = 'CREDIT_TIME_SERVED' if 'CREDIT_TIME_SERVED' in jailed.columns else None
    cts_median = None
    cts_covers_pct = None
    if cts_col:
        cts = jailed[cts_col].dropna()
        cts_median = float(cts.median()) if len(cts) > 0 else None
        # % where CTS >= max term
        both = jailed[['MAXIMUM_TERM_DURATION_DAYS', cts_col]].dropna()
        if len(both) > 0:
            covers = (both[cts_col] >= both['MAXIMUM_TERM_DURATION_DAYS']).sum()
            cts_covers_pct = round(covers / len(both) * 100, 1)
        print(f"  Median credit time served: {cts_median} days")
        print(f"  % where CTS >= max term: {cts_covers_pct}%")
    else:
        print(f"  CREDIT_TIME_SERVED column not found")
        # Check what columns exist related to credit
        credit_cols = [c for c in jailed.columns if 'CREDIT' in c.upper() or 'TIME_SERVED' in c.upper()]
        print(f"  Credit-related columns: {credit_cols}")

    results_q2.append({
        'county': county,
        'n': n,
        'term_median': term_median,
        'pct_1_2': float(bucket_pcts.get('1-2', 0)),
        'pct_3_30': float(bucket_pcts.get('3-30', 0)),
        'pct_31_90': float(bucket_pcts.get('31-90', 0)),
        'pct_91_180': float(bucket_pcts.get('91-180', 0)),
        'pct_181_365': float(bucket_pcts.get('181-365', 0)),
        'pct_365plus': float(bucket_pcts.get('365+', 0)),
        'cts_median': cts_median,
        'cts_covers_pct': cts_covers_pct
    })

# ---- Also compute Escambia and Marion for Query 3 ----
print("\n\n=== ESCAMBIA AND MARION (for Query 3) ===")
results_q3_data = {}
for county in ['Escambia', 'Marion']:
    sub = df_cases[df_cases['COUNTY_DESCRIPTION'] == county]
    n = len(sub)
    if n == 0:
        print(f"{county}: NO DATA")
        results_q3_data[county] = None
        continue
    jail_pct = round((sub['confinement_type'] == 'jail').sum() / n * 100, 2)
    prison_pct = round((sub['confinement_type'] == 'prison').sum() / n * 100, 2)
    prob_only = ((sub['confinement_type'] == 'none') &
                 (sub['SENTENCE_PROBATION_DURATION_DAYS'] > 0)).sum()
    prob_only_pct = round(prob_only / n * 100, 2)
    fine_mean = round(float(sub.loc[sub['FINE'] > 0, 'FINE'].mean()), 2) if (sub['FINE'] > 0).any() else None
    cost_mean = round(float(sub.loc[sub['COURT_COST'] > 0, 'COURT_COST'].mean()), 2) if (sub['COURT_COST'] > 0).any() else None
    results_q3_data[county] = {
        'n': n, 'jail_pct': jail_pct, 'prison_pct': prison_pct,
        'prob_only_pct': prob_only_pct, 'fine_mean': fine_mean, 'cost_mean': cost_mean
    }
    print(f"{county}: n={n}, Jail={jail_pct}%, Prison={prison_pct}%, ProbOnly={prob_only_pct}%, AvgFine=${fine_mean}, AvgCost=${cost_mean}")

# Also Duval for comparison
for county in ['Duval']:
    sub = df_cases[df_cases['COUNTY_DESCRIPTION'] == county]
    n = len(sub)
    jail_pct = round((sub['confinement_type'] == 'jail').sum() / n * 100, 2)
    prison_pct = round((sub['confinement_type'] == 'prison').sum() / n * 100, 2)
    prob_only = ((sub['confinement_type'] == 'none') &
                 (sub['SENTENCE_PROBATION_DURATION_DAYS'] > 0)).sum()
    prob_only_pct = round(prob_only / n * 100, 2)
    fine_mean = round(float(sub.loc[sub['FINE'] > 0, 'FINE'].mean()), 2) if (sub['FINE'] > 0).any() else None
    cost_mean = round(float(sub.loc[sub['COURT_COST'] > 0, 'COURT_COST'].mean()), 2) if (sub['COURT_COST'] > 0).any() else None
    results_q3_data[county] = {
        'n': n, 'jail_pct': jail_pct, 'prison_pct': prison_pct,
        'prob_only_pct': prob_only_pct, 'fine_mean': fine_mean, 'cost_mean': cost_mean
    }
    print(f"{county}: n={n}, Jail={jail_pct}%, Prison={prison_pct}%, ProbOnly={prob_only_pct}%, AvgFine=${fine_mean}, AvgCost=${cost_mean}")

# Save all results
all_results = {
    'query1_severity': results_q1,
    'query2_jail_distribution': results_q2,
    'query3_county_data': results_q3_data
}
out_path = os.path.join(OUTPUT_DIR, 'severity_jail_results.json')
with open(out_path, 'w') as f:
    json.dump(all_results, f, indent=2)

print("\nSaved to severity_jail_results.json")
print("Done!")
