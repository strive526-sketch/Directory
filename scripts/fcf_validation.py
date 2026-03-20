"""
FCF Validation Queries
Filters: statute 316.193% (excl .1935, .1939)
         Disposition IN ('Adjudicated Guilty', 'Adjudication Withheld')
         DISPOSITION_DATE between 2023-01-01 and 2025-12-31
Queries: Hernando, Pinellas, Duval, Statewide
"""
import zipfile, pandas as pd, numpy as np, json, os
from config import ZIP_PATH, OUTPUT_DIR, CHUNK_SIZE

TARGET_COUNTIES = {'Hernando', 'Pinellas', 'Duval'}
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
                f, chunksize=CHUNK_SIZE, dtype=str, low_memory=False,
                usecols=['STATUTE', 'Disposition', 'COUNTY_DESCRIPTION',
                         'DISPOSITION_DATE', 'SENTENCE_CONFINEMENT',
                         'SENTENCE_PROBATION_DURATION_DAYS', 'FINE', 'COURT_COST',
                         'UNIQUE_CORRELATION_ID', 'MAXIMUM_TERM_DURATION_DAYS']
            ):
                for col in chunk.columns:
                    chunk[col] = chunk[col].fillna('').str.strip()

                # DUI filter
                mask_dui = (
                    chunk['STATUTE'].str.startswith('316.193', na=False) &
                    ~chunk['STATUTE'].str.startswith('316.1935', na=False) &
                    ~chunk['STATUTE'].str.startswith('316.1939', na=False)
                )
                # Disposition filter
                mask_disp = chunk['Disposition'].isin(TARGET_DISPS)

                # Date filter
                chunk['_date'] = pd.to_datetime(chunk['DISPOSITION_DATE'], errors='coerce')
                mask_date = (chunk['_date'] >= DATE_MIN) & (chunk['_date'] <= DATE_MAX)

                filtered = chunk[mask_dui & mask_disp & mask_date].copy()
                if len(filtered) > 0:
                    chunks.append(filtered)

df = pd.concat(chunks, ignore_index=True)
print(f"\nTotal filtered rows (all counties, 2023-2025): {len(df)}", flush=True)

# Convert numeric fields
for col in ['SENTENCE_PROBATION_DURATION_DAYS', 'FINE', 'COURT_COST', 'MAXIMUM_TERM_DURATION_DAYS']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Confinement classification
PRISON_VALS = {'State Prison Facility', 'State Prison', 'Prison', 'DOC', 'Florida Department of Corrections'}
JAIL_VALS = {'County Jail', 'Jail', 'County Detention', 'County Correctional Facility',
             'Jail/County Detention Facility', 'County Jail Facility'}

def classify_confinement(val):
    if pd.isna(val) or val == '' or val in {'Not Available', 'N/A', 'NA', 'None', 'NULL'}:
        return 'none'
    v = str(val).strip()
    if any(p.lower() in v.lower() for p in ['state prison', 'prison facility', 'doc']):
        return 'prison'
    if any(j.lower() in v.lower() for j in ['county jail', 'jail']):
        return 'jail'
    return 'other_confinement'

df['confinement_type'] = df['SENTENCE_CONFINEMENT'].apply(classify_confinement)

# Print unique confinement values for inspection
print("\nUnique SENTENCE_CONFINEMENT values (top 20):")
print(df['SENTENCE_CONFINEMENT'].value_counts().head(20).to_string())

def run_query(subset, label):
    n = len(subset)
    if n == 0:
        print(f"\n{label}: NO DATA")
        return None

    # Deduplicate to case level (take first row per UNIQUE_CORRELATION_ID)
    # Since all charges in a case should have same disposition, this is safe
    case_df = subset.drop_duplicates('UNIQUE_CORRELATION_ID')
    n_cases = len(case_df)

    guilty = (case_df['Disposition'] == 'Adjudicated Guilty').sum()
    withheld = (case_df['Disposition'] == 'Adjudication Withheld').sum()

    prison_n = (case_df['confinement_type'] == 'prison').sum()
    jail_n = (case_df['confinement_type'] == 'jail').sum()
    other_conf_n = (case_df['confinement_type'] == 'other_confinement').sum()
    no_conf_n = (case_df['confinement_type'] == 'none').sum()

    # Probation only: no confinement but probation > 0
    prob_only_n = (
        (case_df['confinement_type'] == 'none') &
        (case_df['SENTENCE_PROBATION_DURATION_DAYS'] > 0)
    ).sum()

    # Fine median (where > 0)
    fine_vals = case_df.loc[case_df['FINE'] > 0, 'FINE']
    fine_median = float(fine_vals.median()) if len(fine_vals) > 0 else None
    fine_mean = float(fine_vals.mean()) if len(fine_vals) > 0 else None

    # Court cost median (where > 0)
    cost_vals = case_df.loc[case_df['COURT_COST'] > 0, 'COURT_COST']
    cost_median = float(cost_vals.median()) if len(cost_vals) > 0 else None
    cost_mean = float(cost_vals.mean()) if len(cost_vals) > 0 else None

    # Max term median (where > 0) - for avg sentence length
    term_vals = case_df.loc[case_df['MAXIMUM_TERM_DURATION_DAYS'] > 0, 'MAXIMUM_TERM_DURATION_DAYS']
    term_median_days = float(term_vals.median()) if len(term_vals) > 0 else None
    term_mean_days = float(term_vals.mean()) if len(term_vals) > 0 else None

    result = {
        'label': label,
        'total_rows': int(n),
        'unique_cases': int(n_cases),
        'adjudicated_guilty': int(guilty),
        'adjudication_withheld': int(withheld),
        'prison_n': int(prison_n),
        'prison_pct': round(prison_n / n_cases * 100, 2),
        'jail_n': int(jail_n),
        'jail_pct': round(jail_n / n_cases * 100, 2),
        'other_conf_n': int(other_conf_n),
        'other_conf_pct': round(other_conf_n / n_cases * 100, 2),
        'no_conf_n': int(no_conf_n),
        'no_conf_pct': round(no_conf_n / n_cases * 100, 2),
        'prob_only_n': int(prob_only_n),
        'prob_only_pct': round(prob_only_n / n_cases * 100, 2),
        'fine_n': int(len(fine_vals)),
        'fine_median': round(fine_median, 2) if fine_median else None,
        'fine_mean': round(fine_mean, 2) if fine_mean else None,
        'cost_n': int(len(cost_vals)),
        'cost_median': round(cost_median, 2) if cost_median else None,
        'cost_mean': round(cost_mean, 2) if cost_mean else None,
        'term_n': int(len(term_vals)),
        'term_median_days': round(term_median_days, 1) if term_median_days else None,
        'term_mean_days': round(term_mean_days, 1) if term_mean_days else None,
        'term_mean_months': round(term_mean_days / 30.44, 2) if term_mean_days else None,
    }

    print(f"\n=== {label} ===")
    print(f"  Total charge rows: {n}, Unique cases: {n_cases}")
    print(f"  Guilty: {guilty}, Withheld: {withheld}")
    print(f"  Prison: {prison_n} ({result['prison_pct']}%)")
    print(f"  Jail: {jail_n} ({result['jail_pct']}%)")
    print(f"  Other confinement: {other_conf_n} ({result['other_conf_pct']}%)")
    print(f"  No confinement: {no_conf_n} ({result['no_conf_pct']}%)")
    print(f"  Prob only (no conf, prob>0): {prob_only_n} ({result['prob_only_pct']}%)")
    print(f"  Fine median: ${fine_median}, mean: ${fine_mean} (n={len(fine_vals)})")
    print(f"  Court cost median: ${cost_median}, mean: ${cost_mean} (n={len(cost_vals)})")
    print(f"  Max term median: {term_median_days} days, mean: {term_mean_days} days ({result['term_mean_months']} months)")

    return result

results = {}

# Query 1: Hernando
hernando_df = df[df['COUNTY_DESCRIPTION'] == 'Hernando']
results['Hernando'] = run_query(hernando_df, 'Hernando County')

# Query 2: Pinellas and Duval
pinellas_df = df[df['COUNTY_DESCRIPTION'] == 'Pinellas']
results['Pinellas'] = run_query(pinellas_df, 'Pinellas County')

duval_df = df[df['COUNTY_DESCRIPTION'] == 'Duval']
results['Duval'] = run_query(duval_df, 'Duval County')

# Query 3: Statewide
results['Statewide'] = run_query(df, 'Statewide')

out_path = os.path.join(OUTPUT_DIR, 'fcf_validation_results.json')
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)

print("\nSaved to fcf_validation_results.json")
print("Done!")
