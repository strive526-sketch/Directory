"""
DUI Subset Analysis:
- Method A: FCIC_Category == "DUI-Unlawful Blood Alcohol"
- Method B: STATUTE starts with '316.193' excluding 316.1935 and 316.1939
- Statewide disposition distribution (all categories)
- Disposition by county
- County coverage (which of 67 are present/missing)
- Temporal distribution by year
"""

import zipfile, io, pandas as pd, numpy as np, json, os
from collections import Counter, defaultdict
from config import ZIP_PATH, OUTPUT_DIR, MISSING_VALS

# Florida's 67 counties
FL_COUNTIES = {
    "Alachua","Baker","Bay","Bradford","Brevard","Broward","Calhoun","Charlotte","Citrus",
    "Clay","Collier","Columbia","DeSoto","Dixie","Duval","Escambia","Flagler","Franklin",
    "Gadsden","Gilchrist","Glades","Gulf","Hamilton","Hardee","Hendry","Hernando",
    "Highlands","Hillsborough","Holmes","Indian River","Jackson","Jefferson","Lafayette",
    "Lake","Lee","Leon","Levy","Liberty","Madison","Manatee","Marion","Martin","Miami-Dade",
    "Monroe","Nassau","Okaloosa","Okeechobee","Orange","Osceola","Palm Beach","Pasco",
    "Pinellas","Polk","Putnam","Santa Rosa","Sarasota","Seminole","St. Johns","St. Lucie",
    "Sumter","Suwannee","Taylor","Union","Volusia","Wakulla","Walton","Washington"
}

print("Starting DUI subset analysis...", flush=True)

# Accumulators
method_a_count = 0
method_b_count = 0
a_not_b_count = 0  # in A but not B
b_not_a_count = 0  # in B but not A
a_not_b_statutes = Counter()
b_not_a_fcic = Counter()

# For the "clean" DUI subset (Method B, excluding 316.1935 and 316.1939)
dui_disposition = Counter()
dui_county_disposition = defaultdict(Counter)
dui_year = Counter()
dui_county_total = Counter()
all_county_total = Counter()
dui_fcic_values = Counter()

total_rows = 0

CHUNK_SIZE = 200000

with zipfile.ZipFile(ZIP_PATH) as z:
    for fname in sorted(z.namelist()):
        print(f"Processing {fname}...", flush=True)
        with z.open(fname) as f:
            for chunk in pd.read_csv(f, chunksize=CHUNK_SIZE, dtype=str, low_memory=False):
                total_rows += len(chunk)

                # Normalize
                chunk['STATUTE'] = chunk['STATUTE'].fillna('').str.strip()
                chunk['FCIC_Category'] = chunk['FCIC_Category'].fillna('').str.strip()
                chunk['Disposition'] = chunk['Disposition'].fillna('').str.strip()
                chunk['COUNTY_DESCRIPTION'] = chunk['COUNTY_DESCRIPTION'].fillna('').str.strip()
                chunk['DISPOSITION_DATE'] = chunk['DISPOSITION_DATE'].fillna('').str.strip()

                # Method A: FCIC_Category == "DUI-Unlawful Blood Alcohol"
                mask_a = chunk['FCIC_Category'] == 'DUI-Unlawful Blood Alcohol'

                # Method B: STATUTE starts with '316.193' but NOT '316.1935' or '316.1939'
                mask_b_raw = chunk['STATUTE'].str.startswith('316.193', na=False)
                mask_b_exclude = (
                    chunk['STATUTE'].str.startswith('316.1935', na=False) |
                    chunk['STATUTE'].str.startswith('316.1939', na=False)
                )
                mask_b = mask_b_raw & ~mask_b_exclude

                method_a_count += int(mask_a.sum())
                method_b_count += int(mask_b.sum())

                # A but not B
                a_not_b = mask_a & ~mask_b
                a_not_b_count += int(a_not_b.sum())
                a_not_b_statutes.update(chunk.loc[a_not_b, 'STATUTE'].value_counts().to_dict())

                # B but not A
                b_not_a = mask_b & ~mask_a
                b_not_a_count += int(b_not_a.sum())
                b_not_a_fcic.update(chunk.loc[b_not_a, 'FCIC_Category'].value_counts().to_dict())

                # Use Method B as the clean DUI subset
                dui_chunk = chunk[mask_b]

                # Disposition distribution
                dui_disposition.update(dui_chunk['Disposition'].value_counts().to_dict())

                # County totals (all records)
                all_county_total.update(chunk['COUNTY_DESCRIPTION'].value_counts().to_dict())

                # DUI county distribution
                dui_county_total.update(dui_chunk['COUNTY_DESCRIPTION'].value_counts().to_dict())

                # DUI county x disposition
                for county, grp in dui_chunk.groupby('COUNTY_DESCRIPTION'):
                    dui_county_disposition[county].update(grp['Disposition'].value_counts().to_dict())

                # DUI temporal distribution
                try:
                    dates = pd.to_datetime(dui_chunk['DISPOSITION_DATE'], errors='coerce')
                    years = dates.dt.year.dropna().astype(int).value_counts().to_dict()
                    dui_year.update({int(k): v for k, v in years.items()})
                except Exception:
                    pass

                # FCIC values in DUI B subset
                dui_fcic_values.update(dui_chunk['FCIC_Category'].value_counts().to_dict())

print(f"\nTotal rows: {total_rows}", flush=True)
print(f"Method A count: {method_a_count}", flush=True)
print(f"Method B count: {method_b_count}", flush=True)
print(f"A not B: {a_not_b_count}", flush=True)
print(f"B not A: {b_not_a_count}", flush=True)

# County coverage analysis
counties_in_data = set(k for k in all_county_total.keys() if k and k not in MISSING_VALS)
dui_counties_in_data = set(k for k in dui_county_total.keys() if k and k not in MISSING_VALS)

# Normalize county names for comparison
def normalize_county(name):
    return name.strip().title()

counties_normalized = {normalize_county(c) for c in counties_in_data}
fl_counties_normalized = {normalize_county(c) for c in FL_COUNTIES}
missing_counties = fl_counties_normalized - counties_normalized

print(f"\nCounties in data: {len(counties_normalized)}", flush=True)
print(f"Missing counties: {sorted(missing_counties)}", flush=True)

# Save results
results = {
    'total_rows': total_rows,
    'method_a_count': method_a_count,
    'method_b_count': method_b_count,
    'a_not_b_count': a_not_b_count,
    'b_not_a_count': b_not_a_count,
    'a_not_b_top_statutes': a_not_b_statutes.most_common(20),
    'b_not_a_top_fcic': b_not_a_fcic.most_common(20),
    'dui_disposition': dict(dui_disposition.most_common()),
    'dui_county_total': dict(sorted(dui_county_total.items(), key=lambda x: -x[1])),
    'dui_county_disposition': {k: dict(v) for k, v in dui_county_disposition.items()},
    'dui_year': dict(sorted(dui_year.items())),
    'all_county_total': dict(sorted(all_county_total.items(), key=lambda x: -x[1])),
    'counties_in_data': sorted(counties_normalized),
    'missing_counties': sorted(missing_counties),
    'dui_fcic_values': dict(dui_fcic_values.most_common()),
}

out_path = os.path.join(OUTPUT_DIR, 'dui_analysis_results.json')
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\nSaved to {out_path}", flush=True)
print("Done!", flush=True)
