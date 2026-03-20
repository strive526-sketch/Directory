"""
Five feasibility queries on the full CJDT Clerk dataset.
Saves each query result to a separate JSON file immediately after completion.
"""
import zipfile, json, sys, os
import pandas as pd
import numpy as np
from config import ZIP_PATH, OUTPUT_DIR
OUT_DIR = OUTPUT_DIR + os.sep

def log(msg):
    print(msg, flush=True)
    sys.stdout.flush()

log("Loading full Clerk dataset...")
chunks = []
with zipfile.ZipFile(ZIP_PATH) as z:
    for name in sorted(z.namelist()):
        if not name.endswith(".csv"):
            continue
        with z.open(name) as f:
            chunk = pd.read_csv(f, dtype=str, low_memory=False)
            chunks.append(chunk)
            log(f"  {name}: {len(chunk):,} rows")

df = pd.concat(chunks, ignore_index=True)
log(f"Total rows: {len(df):,}")

# Normalise column names we know are mixed-case
# Disposition -> DISPOSITION for convenience
df["DISPOSITION"] = df["Disposition"]

# DUI filter (exclude .1935 and .1939)
dui_mask = (
    df["STATUTE"].str.startswith("316.193", na=False) &
    ~df["STATUTE"].str.startswith("316.1935", na=False) &
    ~df["STATUTE"].str.startswith("316.1939", na=False)
)
dui = df[dui_mask].copy()
log(f"DUI records: {len(dui):,}")

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 1: Date fields
# ─────────────────────────────────────────────────────────────────────────────
log("\n=== Q1: Date fields ===")

date_cols = [c for c in df.columns if any(kw in c.upper() for kw in
             ["DATE","FILE","ARREST","ARRAIGN","CREATE","OPEN","RECEIV","SUBMIT"])]
log(f"Date-related columns: {date_cols}")

dui["DISP_DATE_p"] = pd.to_datetime(dui["DISPOSITION_DATE"], errors="coerce")
dui["SENT_DATE_p"] = pd.to_datetime(dui["SENTENCING_DATE"],  errors="coerce")

# SENTENCING_DATE -> DISPOSITION_DATE gap
valid = dui[["SENT_DATE_p","DISP_DATE_p"]].dropna()
days = (valid["DISP_DATE_p"] - valid["SENT_DATE_p"]).dt.days
days_clean = days[(days.abs() < 3650)]
log(f"SENTENCING->DISPOSITION valid pairs: {len(days_clean):,}")
log(f"Median gap: {days_clean.median():.0f} days  |  Mean: {days_clean.mean():.1f} days")

# Top 5 counties by SENTENCING->DISPOSITION gap
merged = dui.loc[days_clean.index, ["COUNTY_DESCRIPTION"]].copy()
merged["days"] = days_clean
top5 = (merged.groupby("COUNTY_DESCRIPTION")["days"]
        .agg(median="median", count="count")
        .query("count >= 50")
        .sort_values("count", ascending=False)
        .head(5))
log(top5.to_string())

q1 = {
    "date_columns_found": date_cols,
    "note": "Only DISPOSITION_DATE and SENTENCING_DATE exist. No filing/arrest/arraignment date.",
    "sentencing_to_disposition_median_days": float(days_clean.median()),
    "sentencing_to_disposition_mean_days": round(float(days_clean.mean()), 1),
    "valid_pairs": int(len(days_clean)),
    "top5_counties": top5.reset_index().to_dict(orient="records")
}
with open(OUT_DIR + "q1_results.json", "w") as f:
    json.dump(q1, f, indent=2, default=str)
log("Q1 saved.")

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 2: Financial burden
# ─────────────────────────────────────────────────────────────────────────────
log("\n=== Q2: Financial burden ===")

conv = dui[dui["DISPOSITION"].isin(["Adjudicated Guilty","Adjudication Withheld"])].copy()
log(f"DUI convictions: {len(conv):,}")

conv["FINE_n"]  = pd.to_numeric(conv["FINE"],       errors="coerce")
conv["COST_n"]  = pd.to_numeric(conv["COURT_COST"], errors="coerce")
conv["TOTAL"]   = conv["FINE_n"].fillna(0) + conv["COST_n"].fillna(0)

both_pop = conv["FINE_n"].notna() & conv["COST_n"].notna()
log(f"Both fields populated: {both_pop.sum():,} ({both_pop.mean()*100:.1f}%)")

conv_both = conv[both_pop].copy()

def county_fin(g):
    return pd.Series({
        "median_total": g["TOTAL"].median(),
        "mean_total":   g["TOTAL"].mean(),
        "case_count":   len(g),
        "pct_both_pop": 100.0  # already filtered to both-populated
    })

fin_all = conv.groupby("COUNTY_DESCRIPTION").apply(
    lambda g: pd.Series({
        "median_total": g.loc[g["FINE_n"].notna() & g["COST_n"].notna(), "TOTAL"].median()
                        if (g["FINE_n"].notna() & g["COST_n"].notna()).any() else None,
        "mean_total":   g.loc[g["FINE_n"].notna() & g["COST_n"].notna(), "TOTAL"].mean()
                        if (g["FINE_n"].notna() & g["COST_n"].notna()).any() else None,
        "conv_cases":   len(g),
        "pct_both_pop": (g["FINE_n"].notna() & g["COST_n"].notna()).mean() * 100
    }),
    include_groups=False
).sort_values("conv_cases", ascending=False).head(20)

log(fin_all.to_string())

q2 = {
    "statewide_both_pop_pct": round(float(both_pop.mean()*100), 1),
    "statewide_median_total": float(conv_both["TOTAL"].median()),
    "statewide_mean_total":   round(float(conv_both["TOTAL"].mean()), 2),
    "by_county_top20": fin_all.reset_index().to_dict(orient="records")
}
with open(OUT_DIR + "q2_results.json", "w") as f:
    json.dump(q2, f, indent=2, default=str)
log("Q2 saved.")

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 3: Non-conviction rates
# ─────────────────────────────────────────────────────────────────────────────
log("\n=== Q3: Non-conviction rates ===")

top20_counties = (dui.groupby("COUNTY_DESCRIPTION").size()
                  .sort_values(ascending=False).head(20).index.tolist())
dui3 = dui[dui["COUNTY_DESCRIPTION"].isin(top20_counties)].copy()

def classify_disp(d):
    if pd.isna(d): return "Other"
    d = str(d).strip()
    if d in ("Adjudicated Guilty","Adjudication Withheld"): return "Conviction"
    if any(kw in d for kw in ("Dismiss","Nolle","No Action","Nol Pros")): return "Dismissed"
    if any(kw in d for kw in ("Diversion","Pretrial","PTI","Deferred")): return "Diversion"
    if "Acquit" in d: return "Acquitted"
    return "Other"

dui3["DISP_CLASS"] = dui3["DISPOSITION"].apply(classify_disp)

pivot = (dui3.groupby(["COUNTY_DESCRIPTION","DISP_CLASS"])
         .size().unstack(fill_value=0))
for col in ["Conviction","Dismissed","Diversion","Acquitted","Other"]:
    if col not in pivot.columns:
        pivot[col] = 0

pivot["Total"] = pivot.sum(axis=1)
for col in ["Conviction","Dismissed","Diversion","Acquitted"]:
    pivot[col+"_pct"] = (pivot[col] / pivot["Total"] * 100).round(1)
pivot["NonConv_pct"] = (pivot["Dismissed_pct"] + pivot["Diversion_pct"] + pivot["Acquitted_pct"])
pivot = pivot.sort_values("Total", ascending=False)
log(pivot[["Total","Conviction_pct","Dismissed_pct","Diversion_pct","Acquitted_pct","NonConv_pct"]].to_string())

q3 = pivot.reset_index()[["COUNTY_DESCRIPTION","Total","Conviction_pct","Dismissed_pct",
                           "Diversion_pct","Acquitted_pct","NonConv_pct"]].to_dict(orient="records")
with open(OUT_DIR + "q3_results.json", "w") as f:
    json.dump(q3, f, indent=2, default=str)
log("Q3 saved.")

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 4: Charge stacking
# ─────────────────────────────────────────────────────────────────────────────
log("\n=== Q4: Charge stacking ===")

dui_uids = set(dui["UNIQUE_CORRELATION_ID"].dropna().unique())
log(f"Unique DUI case UIDs: {len(dui_uids):,}")

# All charges on cases that have at least one DUI charge
dui_cases = df[df["UNIQUE_CORRELATION_ID"].isin(dui_uids)].copy()
charges_per_case = (dui_cases.groupby("UNIQUE_CORRELATION_ID")
                    .agg(charge_count=("STATUTE","count"),
                         county=("COUNTY_DESCRIPTION","first")))

sw_avg = float(charges_per_case["charge_count"].mean())
sw_med = float(charges_per_case["charge_count"].median())
log(f"Statewide avg: {sw_avg:.2f}  median: {sw_med:.1f}")

stacking = (charges_per_case.groupby("county")["charge_count"]
            .agg(avg_charges="mean", median_charges="median", case_count="count")
            .sort_values("case_count", ascending=False)
            .head(20))
stacking["avg_charges"] = stacking["avg_charges"].round(2)
log(stacking.to_string())

q4 = {
    "statewide_avg_charges": round(sw_avg, 2),
    "statewide_median_charges": sw_med,
    "by_county_top20": stacking.reset_index().to_dict(orient="records")
}
with open(OUT_DIR + "q4_results.json", "w") as f:
    json.dump(q4, f, indent=2, default=str)
log("Q4 saved.")

# ─────────────────────────────────────────────────────────────────────────────
# QUERY 5: Refusal analysis (316.1939)
# ─────────────────────────────────────────────────────────────────────────────
log("\n=== Q5: Refusal (316.1939) ===")

refusal = df[df["STATUTE"].str.startswith("316.1939", na=False)].copy()
log(f"316.1939 records: {len(refusal):,}")

if len(refusal) > 0:
    ref_disp_pct = refusal["DISPOSITION"].value_counts(normalize=True).mul(100).round(1).head(10)
    dui_disp_pct = dui["DISPOSITION"].value_counts(normalize=True).mul(100).round(1).head(10)
    log("Refusal dispositions:\n" + ref_disp_pct.to_string())
    log("DUI dispositions:\n" + dui_disp_pct.to_string())

    ref_uids = set(refusal["UNIQUE_CORRELATION_ID"].dropna().unique())
    co_occur = len(ref_uids & dui_uids)
    co_pct   = co_occur / len(ref_uids) * 100 if ref_uids else 0
    log(f"Refusal UIDs: {len(ref_uids):,}")
    log(f"Co-occurring with DUI: {co_occur:,} ({co_pct:.1f}%)")

    q5 = {
        "total_records": int(len(refusal)),
        "unique_uids": int(len(ref_uids)),
        "co_occur_with_dui": int(co_occur),
        "co_occur_pct": round(co_pct, 1),
        "refusal_disposition_pct": ref_disp_pct.to_dict(),
        "dui_disposition_pct": dui_disp_pct.to_dict()
    }
else:
    q5 = {"total_records": 0, "note": "No 316.1939 records found"}

with open(OUT_DIR + "q5_results.json", "w") as f:
    json.dump(q5, f, indent=2, default=str)
log("Q5 saved.")

log("\n=== ALL DONE ===")
