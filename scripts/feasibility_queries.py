"""
Five feasibility queries on the full CJDT Clerk dataset.
All queries use vectorized pandas operations for speed.
"""
import zipfile, io, json
import pandas as pd
import numpy as np

ZIP_PATH = "/home/ubuntu/cjdt/CjdtClerkCase.zip"
SAO_ZIP  = "/home/ubuntu/sao_data/CjdtSAOCase.zip"

print("Loading full Clerk dataset...")

chunks = []
with zipfile.ZipFile(ZIP_PATH) as z:
    for name in sorted(z.namelist()):
        if not name.endswith(".csv"):
            continue
        with z.open(name) as f:
            df = pd.read_csv(f, dtype=str, low_memory=False)
            chunks.append(df)
            print(f"  Loaded {name}: {len(df):,} rows")

df = pd.concat(chunks, ignore_index=True)
print(f"Total rows: {len(df):,}")
print(f"Columns: {list(df.columns)}")

results = {}

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 1: Date fields and timeline analysis
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== QUERY 1: Date fields ===")

date_cols = [c for c in df.columns if any(kw in c.upper() for kw in
             ["DATE","FILE","ARREST","ARRAIGN","CREATE","OPEN","RECEIV","SUBMIT"])]
print(f"Date-related columns found: {date_cols}")

# Parse all date columns
for col in date_cols:
    df[col + "_parsed"] = pd.to_datetime(df[col], errors="coerce")

# DUI filter
dui_mask = (
    df["STATUTE"].str.startswith("316.193", na=False) &
    ~df["STATUTE"].str.startswith("316.1935", na=False) &
    ~df["STATUTE"].str.startswith("316.1939", na=False)
)
dui = df[dui_mask].copy()
print(f"DUI records: {len(dui):,}")

# Compute timeline metrics for any non-DISPOSITION_DATE date column
timeline_results = {}
disp_col = "DISPOSITION_DATE_parsed"

for col in date_cols:
    parsed = col + "_parsed"
    if parsed == disp_col or parsed not in dui.columns:
        continue
    valid = dui[[parsed, disp_col]].dropna()
    if len(valid) < 100:
        continue
    days = (valid[disp_col] - valid[parsed]).dt.days
    days = days[(days >= 0) & (days < 3650)]  # sanity: 0-10 years
    if len(days) < 100:
        continue
    statewide_median = int(days.median())
    # Top 5 counties
    merged = dui.loc[days.index, ["COUNTY_DESCRIPTION"]].copy()
    merged["days"] = days
    top5 = (merged.groupby("COUNTY_DESCRIPTION")["days"]
            .agg(["median","count"])
            .query("count >= 50")
            .sort_values("count", ascending=False)
            .head(5))
    timeline_results[col] = {
        "statewide_median_days": statewide_median,
        "valid_pairs": int(len(days)),
        "top5_counties": top5.reset_index().to_dict(orient="records")
    }
    print(f"  {col} -> disposition: median {statewide_median} days (n={len(days):,})")

results["q1_date_columns"] = date_cols
results["q1_timeline"] = timeline_results

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 2: Financial burden by county
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== QUERY 2: Financial burden ===")

dui2 = dui.copy()
dui2["FINE_num"]       = pd.to_numeric(dui2["FINE"],       errors="coerce")
dui2["COURT_COST_num"] = pd.to_numeric(dui2["COURT_COST"], errors="coerce")

# Disposition filter: guilty / AW only
conv_mask = dui2["Disposition"].isin(["Adjudicated Guilty","Adjudication Withheld"])
dui2 = dui2[conv_mask]
print(f"DUI convictions: {len(dui2):,}")

both_pop = dui2["FINE_num"].notna() & dui2["COURT_COST_num"].notna()
print(f"Both fields populated: {both_pop.sum():,} ({both_pop.mean()*100:.1f}%)")

dui2["TOTAL_FINANCIAL"] = dui2["FINE_num"].fillna(0) + dui2["COURT_COST_num"].fillna(0)
dui2_both = dui2[both_pop].copy()

fin_by_county = (dui2_both.groupby("COUNTY_DESCRIPTION")["TOTAL_FINANCIAL"]
                 .agg(["median","mean","count"])
                 .sort_values("count", ascending=False)
                 .head(20))

# Also compute % both populated per county
pct_both = (dui2.groupby("COUNTY_DESCRIPTION")
            .apply(lambda x: (x["FINE_num"].notna() & x["COURT_COST_num"].notna()).mean() * 100)
            .rename("pct_both_populated"))

fin_by_county = fin_by_county.join(pct_both)
print(fin_by_county.to_string())
results["q2_financial"] = fin_by_county.reset_index().to_dict(orient="records")

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 3: Alternative outcome pathways (non-conviction rate)
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== QUERY 3: Non-conviction rates ===")

dui3 = dui.copy()
# Top 20 counties by DUI volume
top20_counties = (dui3.groupby("COUNTY_DESCRIPTION").size()
                  .sort_values(ascending=False).head(20).index.tolist())
dui3_top = dui3[dui3["COUNTY_DESCRIPTION"].isin(top20_counties)]

def classify_disp(d):
    if pd.isna(d):
        return "Other"
    d = str(d).strip()
    if d in ("Adjudicated Guilty","Adjudication Withheld"):
        return "Conviction"
    if "Dismiss" in d or "Nolle" in d or "No Action" in d:
        return "Dismissed"
    if "Diversion" in d or "Pretrial" in d or "PTI" in d:
        return "Diversion"
    if "Acquit" in d:
        return "Acquitted"
    return "Other"

dui3_top = dui3_top.copy()
dui3_top["DISP_CLASS"] = dui3_top["Disposition"].apply(classify_disp)

outcome_pivot = (dui3_top.groupby(["COUNTY_DESCRIPTION","DISP_CLASS"])
                 .size().unstack(fill_value=0))

# Ensure all columns exist
for col in ["Conviction","Dismissed","Diversion","Acquitted","Other"]:
    if col not in outcome_pivot.columns:
        outcome_pivot[col] = 0

outcome_pivot["Total"] = outcome_pivot.sum(axis=1)
for col in ["Conviction","Dismissed","Diversion","Acquitted"]:
    outcome_pivot[col + "_pct"] = (outcome_pivot[col] / outcome_pivot["Total"] * 100).round(1)

outcome_pivot["NonConviction_pct"] = (
    outcome_pivot["Dismissed_pct"] +
    outcome_pivot["Diversion_pct"] +
    outcome_pivot["Acquitted_pct"]
)
outcome_pivot = outcome_pivot.sort_values("Total", ascending=False)
print(outcome_pivot[["Total","Conviction_pct","Dismissed_pct","Diversion_pct",
                      "Acquitted_pct","NonConviction_pct"]].to_string())
results["q3_outcomes"] = outcome_pivot.reset_index()[
    ["COUNTY_DESCRIPTION","Total","Conviction_pct","Dismissed_pct",
     "Diversion_pct","Acquitted_pct","NonConviction_pct"]
].to_dict(orient="records")

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 4: Charge stacking
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== QUERY 4: Charge stacking ===")

# Use full dataset (not just DUI) to count charges per case
# A "DUI case" = any UNIQUE_CORRELATION_ID that has at least one 316.193 charge
dui_uids = set(dui["UNIQUE_CORRELATION_ID"].dropna().unique())
print(f"Unique DUI case UIDs: {len(dui_uids):,}")

# Count charges per UID across the full dataset
charges_per_case = (df[df["UNIQUE_CORRELATION_ID"].isin(dui_uids)]
                    .groupby("UNIQUE_CORRELATION_ID")
                    .agg(
                        charge_count=("STATUTE","count"),
                        county=("COUNTY_DESCRIPTION","first")
                    ))

statewide_avg = charges_per_case["charge_count"].mean()
statewide_med = charges_per_case["charge_count"].median()
print(f"Statewide avg charges per DUI case: {statewide_avg:.2f}")
print(f"Statewide median charges per DUI case: {statewide_med:.1f}")

stacking_by_county = (charges_per_case.groupby("county")["charge_count"]
                      .agg(["mean","median","count"])
                      .sort_values("count", ascending=False)
                      .head(20))
stacking_by_county.columns = ["avg_charges","median_charges","case_count"]
print(stacking_by_county.to_string())

results["q4_stacking"] = {
    "statewide_avg": round(float(statewide_avg), 2),
    "statewide_median": float(statewide_med),
    "by_county": stacking_by_county.reset_index().to_dict(orient="records")
}

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 5: Refusal analysis (316.1939)
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== QUERY 5: Refusal analysis (316.1939) ===")

refusal = df[df["STATUTE"].str.startswith("316.1939", na=False)].copy()
print(f"316.1939 records: {len(refusal):,}")

if len(refusal) > 0:
    # Disposition distribution
    ref_disp = refusal["Disposition"].value_counts(dropna=False).head(10)
    print("Disposition distribution:")
    print(ref_disp.to_string())

    # Compare to DUI disposition distribution
    dui_disp = dui["Disposition"].value_counts(normalize=True).mul(100).round(1).head(10)
    ref_disp_pct = refusal["Disposition"].value_counts(normalize=True).mul(100).round(1).head(10)

    # Co-occurrence: how many 316.1939 UIDs also have a 316.193 charge?
    ref_uids = set(refusal["UNIQUE_CORRELATION_ID"].dropna().unique())
    co_occur = len(ref_uids & dui_uids)
    co_pct = co_occur / len(ref_uids) * 100 if ref_uids else 0
    print(f"Refusal UIDs: {len(ref_uids):,}")
    print(f"Co-occurring with 316.193 DUI: {co_occur:,} ({co_pct:.1f}%)")

    results["q5_refusal"] = {
        "total_records": int(len(refusal)),
        "unique_uids": int(len(ref_uids)),
        "co_occur_with_dui": int(co_occur),
        "co_occur_pct": round(co_pct, 1),
        "disposition_dist": ref_disp_pct.to_dict(),
        "dui_disposition_dist": dui_disp.to_dict()
    }
else:
    results["q5_refusal"] = {"total_records": 0}

# ─────────────────────────────────────────────────────────────────────────────
# Save results
# ─────────────────────────────────────────────────────────────────────────────
with open("/home/ubuntu/cjdt/feasibility_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)

print("\n=== DONE. Results saved to feasibility_results.json ===")
