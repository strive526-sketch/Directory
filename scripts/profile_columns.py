"""
Full column-by-column profile of the CJDT Clerk Case dataset.
Reads all 5 CSV files (4,092,482 rows total) and computes:
- Data type, total records, completeness (treating null/empty/"Not Available"/"N/A" as missing)
- Unique value count
- Top 10 most frequent values with counts and percentages
- Date fields: min, max, year distribution
- Numeric fields: min, max, mean, median, std
"""

import zipfile, io, pandas as pd, numpy as np, json, sys, os
from collections import defaultdict, Counter
from config import ZIP_PATH, OUTPUT_DIR, MISSING_VALS

# We'll accumulate stats incrementally across chunks to avoid OOM
# Strategy: read each of the 5 files, process in chunks of 100k rows

print("Starting full column profile...", flush=True)

# First pass: get column names from first file
with zipfile.ZipFile(ZIP_PATH) as z:
    names = z.namelist()
    print(f"Files in ZIP: {names}", flush=True)
    with z.open(names[0]) as f:
        header_df = pd.read_csv(f, nrows=0)
        COLUMNS = list(header_df.columns)

print(f"Total columns: {len(COLUMNS)}", flush=True)
print(f"Columns: {COLUMNS}", flush=True)

# Initialize accumulators
total_rows = 0
col_stats = {}
for col in COLUMNS:
    col_stats[col] = {
        'total': 0,
        'non_missing': 0,
        'value_counter': Counter(),
        'numeric_vals': [],  # will store sample for stats
        'is_date': False,
        'is_numeric': False,
        'date_years': Counter(),
        'date_min': None,
        'date_max': None,
        'num_min': None,
        'num_max': None,
        'num_sum': 0.0,
        'num_sum_sq': 0.0,
        'num_count': 0,
        'num_vals_sample': [],  # for median
    }

DATE_COLS = {'DISPOSITION_DATE', 'SENTENCING_DATE'}
NUMERIC_COLS = {'AGE', 'COURT_COST', 'FINE', 'RESTITUTION', 'CREDIT_TIME_SERVED',
                'MAXIMUM_TERM_DURATION_DAYS', 'MINIMUM_TERM_DURATION_DAYS',
                'SENTENCE_COMM_CTRL_DURATION_DAYS', 'SENTENCE_PROBATION_DURATION_DAYS',
                'CHARGE_ID', 'COUNTY_CODE', 'JUDICIAL_CIRCUIT', 'RCC_DISTRICT',
                'PERSON_ID', 'MDM_PERSON_ID'}

CHUNK_SIZE = 200000
file_num = 0

with zipfile.ZipFile(ZIP_PATH) as z:
    for fname in sorted(z.namelist()):
        file_num += 1
        print(f"\nProcessing file {file_num}: {fname}", flush=True)
        with z.open(fname) as f:
            chunk_num = 0
            for chunk in pd.read_csv(f, chunksize=CHUNK_SIZE, dtype=str, low_memory=False):
                chunk_num += 1
                rows_in_chunk = len(chunk)
                total_rows += rows_in_chunk
                print(f"  Chunk {chunk_num}: {rows_in_chunk} rows (total so far: {total_rows})", flush=True)

                for col in COLUMNS:
                    if col not in chunk.columns:
                        continue
                    series = chunk[col]
                    col_stats[col]['total'] += rows_in_chunk

                    # Compute missing: null OR in MISSING_VALS set
                    is_null = series.isna()
                    is_missing_str = series.isin(MISSING_VALS)
                    is_missing = is_null | is_missing_str
                    non_missing_count = (~is_missing).sum()
                    col_stats[col]['non_missing'] += int(non_missing_count)

                    # Value counter (top values) - use non-missing values
                    non_missing_vals = series[~is_missing]
                    col_stats[col]['value_counter'].update(non_missing_vals.value_counts().to_dict())

                    # Date handling
                    if col in DATE_COLS:
                        col_stats[col]['is_date'] = True
                        try:
                            dates = pd.to_datetime(non_missing_vals, errors='coerce')
                            valid_dates = dates.dropna()
                            if len(valid_dates) > 0:
                                years = valid_dates.dt.year.value_counts().to_dict()
                                col_stats[col]['date_years'].update({int(k): v for k, v in years.items()})
                                d_min = valid_dates.min()
                                d_max = valid_dates.max()
                                if col_stats[col]['date_min'] is None or d_min < col_stats[col]['date_min']:
                                    col_stats[col]['date_min'] = d_min
                                if col_stats[col]['date_max'] is None or d_max > col_stats[col]['date_max']:
                                    col_stats[col]['date_max'] = d_max
                        except Exception:
                            pass

                    # Numeric handling
                    if col in NUMERIC_COLS:
                        col_stats[col]['is_numeric'] = True
                        try:
                            nums = pd.to_numeric(non_missing_vals, errors='coerce').dropna()
                            if len(nums) > 0:
                                col_stats[col]['num_count'] += len(nums)
                                col_stats[col]['num_sum'] += float(nums.sum())
                                col_stats[col]['num_sum_sq'] += float((nums**2).sum())
                                n_min = float(nums.min())
                                n_max = float(nums.max())
                                if col_stats[col]['num_min'] is None or n_min < col_stats[col]['num_min']:
                                    col_stats[col]['num_min'] = n_min
                                if col_stats[col]['num_max'] is None or n_max > col_stats[col]['num_max']:
                                    col_stats[col]['num_max'] = n_max
                                # Sample for median (keep up to 50k values)
                                if len(col_stats[col]['num_vals_sample']) < 50000:
                                    col_stats[col]['num_vals_sample'].extend(nums.tolist()[:5000])

                        except Exception:
                            pass

print(f"\nTotal rows processed: {total_rows}", flush=True)

# Compute final stats
print("\nComputing final statistics...", flush=True)
results = {}
for col in COLUMNS:
    s = col_stats[col]
    total = s['total']
    non_missing = s['non_missing']
    missing = total - non_missing
    completeness_pct = (non_missing / total * 100) if total > 0 else 0

    # Top 10 values
    top10 = s['value_counter'].most_common(10)
    top10_formatted = [(v, c, round(c/total*100, 2)) for v, c in top10]

    # Unique count (approximate from counter)
    unique_count = len(s['value_counter'])

    entry = {
        'col': col,
        'total': total,
        'non_missing': non_missing,
        'missing': missing,
        'completeness_pct': round(completeness_pct, 2),
        'unique_count': unique_count,
        'top10': top10_formatted,
        'is_date': s['is_date'],
        'is_numeric': s['is_numeric'],
    }

    if s['is_date']:
        entry['date_min'] = str(s['date_min']) if s['date_min'] else None
        entry['date_max'] = str(s['date_max']) if s['date_max'] else None
        entry['date_years'] = dict(sorted(s['date_years'].items()))

    if s['is_numeric'] and s['num_count'] > 0:
        n = s['num_count']
        mean = s['num_sum'] / n
        variance = (s['num_sum_sq'] / n) - (mean ** 2)
        std = variance ** 0.5 if variance > 0 else 0
        median = float(np.median(s['num_vals_sample'])) if s['num_vals_sample'] else None
        entry['num_min'] = s['num_min']
        entry['num_max'] = s['num_max']
        entry['num_mean'] = round(mean, 4)
        entry['num_median'] = round(median, 4) if median is not None else None
        entry['num_std'] = round(std, 4)
        entry['num_count'] = n

    results[col] = entry

# Save results
out_path = os.path.join(OUTPUT_DIR, 'column_profile_results.json')
with open(out_path, 'w') as f:
    json.dump({'total_rows': total_rows, 'columns': results}, f, indent=2, default=str)

print(f"\nSaved to {out_path}", flush=True)
print("Done!", flush=True)
