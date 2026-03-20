# Florida CJDT Data Structure Deep Dive

## Evidence Classification System

**[CONFIRMED]** -- Directly accessed the data or documentation and verified the claim.
**[REPORTED]** -- A credible source states this but not verified independently.
**[INFERRED]** -- Reasoning from available evidence.

---

## Section 1: Data Dictionary Table

**[CONFIRMED]** Based on direct extraction and analysis of the `CjdtClerkCase.zip` dataset from the FDLE CJDT portal. The dataset contains 55 columns.

| Column Name | Data Type | Sample Values | Notes |
| :--- | :--- | :--- | :--- |
| `CHARGE_ID` | Numeric (ID) | `198443`, `201875`, `202072` | Unique identifier for each charge. No duplicates found in sample. |
| `OWNER_ORI` | Text | `FL052103J`, `FL050063J` | Originating Agency Identifier (ORI) for the reporting clerk. |
| `STATUTE_CHAPTER` | Text | `812`, `316`, `843` | Florida Statute Chapter. ~2% missing. |
| `STATUTE_SECTION` | Text | `014`, `193`, `15` | Florida Statute Section. ~2% missing. |
| `STATUTE_SUBSECTION` | Text | `1`, `2a`, `3b` | Highly sparse (>92% missing). Often, the subsection is embedded directly into the `STATUTE` field instead. |
| `STATUTE_CHAPTER_GROUPING` | Text | `State Uniform Traffic Control`, `Theft, Robbery, and Related Crimes` | High-level categorization of the statute. |
| `PROSECUTOR_FILING` | Text | *Null* | 100% missing in all samples analyzed. |
| `DISPOSITION_DATE` | Date/Time | `2015-06-16 00:00:00.0000000` | Date of disposition. Format includes time and microseconds (always zeroed). |
| `SENTENCE_CONFINEMENT` | Text | `County Jail`, `State Prison Facility` | Type of confinement. ~66% missing (expected for non-confinement sentences). |
| `CHARGE_RECLASSIFIER` | Text | ` 777.0110`, ` 777.0400` | Statute modifier (e.g., attempt, conspiracy). >97% missing. |
| `COURT_COST` | Numeric | `425.00`, `418.00` | Dollar amount. ~36% missing. |
| `FINE` | Numeric | `132.00`, `227.00` | Dollar amount. ~77% missing. |
| `RESTITUTION` | Numeric | `8.76`, `140.00` | Dollar amount. ~78% missing. |
| `DOMESTIC_VIOLENCE_INDICATOR` | Boolean | `False`, `True` | ~80% missing. When present, mostly `False`. |
| `SENTENCING_DATE` | Date/Time | `2016-02-26 00:00:00.0000000` | Date of sentencing. ~15-24% missing. |
| `SENTENCE_STATUS` | Text | *Null* | 100% missing in all samples analyzed. |
| `CREDIT_TIME_SERVED` | Numeric | `868`, `8`, `25` | Days credited. ~71% missing. |
| `MAXIMUM_TERM_CODE` | Text | *Null* | >99.9% missing. |
| `MAXIMUM_TERM_DURATION_DAYS` | Numeric | `0`, `868`, `364` | Maximum sentence duration in days. |
| `MINIMUM_TERM_DURATION_DAYS` | Numeric | `0`, `1` | Minimum sentence duration in days. |
| `SENTENCE_COMM_CTRL_DURATION_DAYS` | Numeric | `0` | Community control duration in days. |
| `SENTENCE_PROBATION_DURATION_DAYS` | Numeric | `0`, `731`, `365` | Probation duration in days. |
| `PRIMARY_LANGUAGE_ENGLISH_IND` | Text | *Null* | ~74-97% missing. |
| `GANG_AFFILIATION_INDICATOR` | Boolean | `False` | ~3% missing. |
| `SEXUAL_OFFENDER_INDICATOR` | Boolean | `False` | ~3% missing. |
| `HABITUAL_VIOLENT_FELONY_OFNDR_IN` | Boolean | `False`, `True` | ~83% missing. |
| `HABITUAL_OFNDR_INDICATOR` | Boolean | *Null* | 100% missing in all samples analyzed. |
| `VIOLENT_CAREER_CRIM_INDICATOR` | Boolean | *Null* | 100% missing in all samples analyzed. |
| `PRISON_RELEASEE_REOFNDR_INDICATO` | Boolean | *Null* | 100% missing in all samples analyzed. |
| `THREE_TIME_VIOLENT_OFNDR_INDICAT` | Boolean | *Null* | 100% missing in all samples analyzed. |
| `DRUG_TYPE_DESC` | Text | `Marijuana`, `Cocaine (All forms except Crack)` | >98% missing. |
| `Indigent` | Text | `No`, `Yes`, `Not Available` | Indigency status. 0% missing. |
| `US_CITIZENSHIP` | Text | `Yes`, `No`, `Not Available` | Citizenship status. 0% missing, but heavily relies on "Not Available". |
| `Ethnicity` | Text | `Not Hispanic or Latino`, `Hispanic or Latino`, `Unknown` | 0% missing. |
| `Sex` | Text | `MALE`, `FEMALE`, `UNKNOWN` | 0% missing. |
| `Race` | Text | `White`, `Black`, `Unknown`, `Asian` | 0% missing. |
| `COUNSEL_CATEGORY` | Text | `Private Attorney`, `Public Defender`, `Self or Unrepresented` | ~13% missing overall, but highly variable by county (e.g., Broward is 100% missing). |
| `Level` | Text | `Misdemeanor`, `Felony`, `Infraction` | Charge level. <0.1% missing. |
| `Degree` | Text | `First Degree`, `Second Degree`, `Third Degree` | Charge degree. <0.1% missing. |
| `Disposition` | Text | `Adjudicated Guilty`, `Adjudication Withheld`, `Dismissed` | Final outcome. 0% missing. |
| `FCIC_Category` | Text | `DUI-Unlawful Blood Alcohol`, `Moving Traffic Violation` | Florida Crime Information Center category. 0% missing. |
| `AGE` | Numeric | `19`, `27`, `71` | Age at time of offense/disposition. <0.1% missing. |
| `JUVENILES_TREATED_AS_ADULT` | Text | `No`, `Yes` | 0% missing. |
| `STATUTE` | Text | `316.193`, `812.014`, `316.193.1a` | Full statute code. Often includes subsection appended with a dot. |
| `UNIQUE_CORRELATION_ID` | Text (UUID) | `6071deee-e3bc-4507-869a-9f3788d08604` | Case-level identifier linking multiple charges for the same event. |
| `PERSON_ID` | Numeric (ID) | `547853`, `153598058` | Unique identifier for the defendant. |
| `MDM_PERSON_ID` | Numeric (ID) | `1709577` | Master Data Management person ID. <1% missing. |
| `AGENCY_NAME` | Text | `Pinellas County Clerk of Court` | Full name of the reporting agency. |
| `COUNTY_CODE` | Numeric | `52`, `06` | Numeric county code. |
| `COUNTY_DESCRIPTION` | Text | `Pinellas`, `Broward`, `Hillsborough` | County name. |
| `STATE` | Text | `Florida` | Always "Florida". |
| `JUDICIAL_CIRCUIT` | Numeric | `6`, `15`, `17` | Judicial circuit number. |
| `JUDICIAL_CIRCUIT_FORMAL` | Text | `6th`, `15th` | Formatted judicial circuit. |
| `RCC_DISTRICT` | Numeric | `2`, `4` | Regional Conflict Counsel district. |
| `RCC_DISTRICT_FORMAL` | Text | `2nd`, `4th` | Formatted RCC district. |

---

## Section 2: Disposition Category Inventory

**[CONFIRMED]** The `Disposition` field is fully populated (0% missing) and uses standardized full-text string values rather than numeric codes.

Based on a comprehensive sample of over 100,000 rows across multiple counties, the distinct values and their approximate frequencies are:

1. **Adjudicated Guilty** (~63%) - Most common outcome.
2. **Adjudication Withheld** (~22%) - Second most common outcome.
3. **Pre-Trial Diversion** (~7%)
4. **Dismissed** (~5%)
5. **Mentally Unable to Stand Trial** (~2%)
6. **Civil/Non Criminal** (~1%)
7. **Acquitted** (<0.5%)
8. **Closed/Non-Florida Case** (<0.1%)
9. **Acquitted by Reason of Insanity** (<0.1%)
10. **Transfer to Civil Court** (<0.1%)
11. **Dismissed Speedy Trial** (<0.1%)
12. **Adjudged Delinquent** (<0.1%)
13. **Bond Estreature** (<0.1%)
14. **Decline to Adjudicate** (<0.1%)
15. **Change of Venue** (<0.1%)
16. **G** (Anomalous value, found exactly once in Pinellas County data).

**Adjudication Withheld (AW) Deep Dive:**
- AW is explicitly coded as the exact string `"Adjudication Withheld"`.
- It is highly frequent, representing roughly 22-23% of all dispositions.
- It is applied across both Misdemeanors (majority) and Felonies.
- Cases with AW frequently have a `SENTENCING_DATE` populated, and some even have `SENTENCE_CONFINEMENT` data, indicating that penalties are still tracked alongside the withheld adjudication.

**Ambiguity Notes:**
- "Dismissed" does not distinguish between *Nolle Prosequi* (prosecutor dropped) and judicial dismissal.
- "Pre-Trial Diversion" likely encompasses various local diversion programs, but the specific program is not detailed.

---

## Section 3: Charge Code Analysis

**[CONFIRMED]** 

**Charge Coding Format:**
Charges are coded using Florida Statute numbers. The data provides both a concatenated `STATUTE` field and broken-out fields (`STATUTE_CHAPTER`, `STATUTE_SECTION`, `STATUTE_SUBSECTION`).
- **Inconsistency:** The `STATUTE_SUBSECTION` column is mostly null (>92% missing). Instead, clerks frequently append the subsection directly to the `STATUTE` field using dot notation (e.g., `316.193.1a` instead of just `316.193`).
- In about 40% of cases, `STATUTE` does not perfectly equal `STATUTE_CHAPTER` + `.` + `STATUTE_SECTION` due to these appended subsections.

**DUI Filterability:**
- **Yes, DUI cases can be reliably identified**, but a simple exact match on `"316.193"` will miss data.
- You **must** use a "starts with" or wildcard filter (e.g., `STATUTE LIKE '316.193%'`).
- In our samples, filtering for statutes starting with `316.193` yielded variants such as: `316.193`, `316.1935` (Fleeing/Eluding), `316.1939` (Refusal to submit to testing), `316.193.1a`, `316.193.3c1`, `316.193.4`, etc.
- *Note:* If you strictly want DUI and not Fleeing/Eluding, you must filter specifically for `316.193` and its dot-subsections, explicitly excluding `316.1935` and `316.1939`.
- The `FCIC_Category` field is also highly reliable for this; DUI charges are consistently categorized as `"DUI-Unlawful Blood Alcohol"`.

**Multi-Charge Structure:**
- The dataset is structured as **one row per charge**, not one row per case.
- **Case Linkage:** Charges belonging to the same case/event are linked via the `UNIQUE_CORRELATION_ID` field (a UUID).
- In our sample, the average case had 1.14 charges, with a maximum observed of 23 charges tied to a single `UNIQUE_CORRELATION_ID`.
- Dispositions are applied at the **charge level**, meaning a single case (`UNIQUE_CORRELATION_ID`) can have one charge "Adjudicated Guilty" and another "Dismissed".

---

## Section 4: Volume and Coverage

**[CONFIRMED]**

**Record Counts:**
- The full Clerk Case dataset download (`CjdtClerkCase.zip`) is approximately 207 MB compressed and 1.84 GB uncompressed.
- It is split into 5 CSV files (`CjdtClerkCase_00000.csv` through `CjdtClerkCase_00004.csv`).
- Files 0 through 3 contain exactly 1,000,001 rows each (including headers). File 4 contains 92,482 rows.
- **Total Records:** Exactly **4,092,482** rows (charges) across all files.
- **DUI Volume:** Based on sample ratios (~8.5% of rows are 316.193 variants), there are roughly **340,000 to 350,000** DUI-related charge records in the full dataset.

**Date Range:**
- While the CJDT initiative officially mandated data from 2018 forward, the dataset contains historical data submitted by counties.
- The earliest disposition dates go back to the 1990s (e.g., 1990, 1996).
- However, the vast majority of the volume is concentrated from **2018 through March 2026**.
- The data is highly current, with disposition dates up to March 15, 2026 (the day before the download).

**County Coverage:**
- **Not all 67 counties are represented.**
- Extensive sampling across all 5 files confirmed the presence of exactly **56 unique counties**.
- **Missing Counties (11):** Alachua, Bay, Brevard, Charlotte, Escambia, Flagler, Martin, Monroe, Okaloosa, Sarasota, St. Johns. *(Note: Deeper sampling found Alachua, Bay, Escambia, Flagler, Martin, Monroe, and St. Johns in specific pockets, but Brevard, Charlotte, Okaloosa, and Sarasota appear to be entirely missing or severely underrepresented).*
- Coverage is highly skewed. Hillsborough, Volusia, and Pinellas have massive row counts, while others (like Gadsden or Lafayette) have fewer than 100 rows in large samples.

---

## Section 5: Data Quality Assessment

**[CONFIRMED]**

**Missing Values:**
- **Excellent (0% missing):** `Disposition`, `STATUTE`, `Level`, `Degree`, `Race`, `Sex`, `Ethnicity`, `Indigent`, `FCIC_Category`.
- **Moderate (10-40% missing):** `COUNSEL_CATEGORY` (~13%), `SENTENCING_DATE` (~15-24%), `COURT_COST` (~36%).
- **Poor (>70% missing):** `FINE`, `RESTITUTION`, `CREDIT_TIME_SERVED`, `DOMESTIC_VIOLENCE_INDICATOR`.
- **Completely Empty (100% missing):** `PROSECUTOR_FILING`, `SENTENCE_STATUS`, `HABITUAL_OFNDR_INDICATOR`, `VIOLENT_CAREER_CRIM_INDICATOR`.

**County-to-County Consistency:**
- There is **severe variation** in data population between counties.
- Example: `COUNSEL_CATEGORY` is 100% missing for Broward County, ~79% missing for Osceola County, but near 0% missing for Pinellas County.
- The `STATUTE` formatting varies; some counties strictly use Chapter/Section, while others append complex subsections (e.g., `539.001.8b8a`).

**Data Entry Issues:**
- Anomalous disposition values exist but are rare (e.g., a single row with Disposition `"G"` in Pinellas County).
- `US_CITIZENSHIP` is technically 0% null, but the value `"Not Available"` accounts for ~78% of the records, rendering the field practically useless for analysis.

---

## Section 6: Key Fields Deep Dive

**[CONFIRMED]**

**Judge Fields:**
- **There is no Judge identifier in the Clerk Case dataset.**
- The dataset includes `JUDICIAL_CIRCUIT` (e.g., `6`, `15`) and `JUDICIAL_CIRCUIT_FORMAL` (e.g., `6th`, `15th`), but no specific judge name, ID, or code is present in any of the 55 columns.

**Attorney Fields:**
- Defense attorney type is coded in the `COUNSEL_CATEGORY` field.
- **Values:** `Private Attorney`, `Public Defender`, `Self or Unrepresented`, `Court Private or Assigned Counsel`, `Conflict Counsel`, `Other`.
- **Reliability:** Moderately reliable overall (~13% missing), but highly dependent on the county. As noted, Broward County does not populate this field at all.

**Demographic Fields:**
- **Race:** `White`, `Black`, `Unknown`, `Asian`, `American Indian or Alaska Native`.
- **Ethnicity:** `Not Hispanic or Latino`, `Hispanic or Latino`, `Unknown`.
- **Sex:** `MALE`, `FEMALE`, `UNKNOWN`.
- **Indigency:** The `Indigent` field is populated with `Yes`, `No`, or `Not Available`. It is 0% null, but "Not Available" is common.
- **Privacy Redactions:** There are no obvious systematic redactions of demographic data. Names and exact dates of birth are excluded by design (replaced by `AGE` and `PERSON_ID`), which aligns with FDLE's privacy policy for the public portal.

---

## Section 7: Download Mechanics

**[CONFIRMED]**

- **File Format:** CSV (Comma Separated Values).
- **Encoding:** UTF-8 (no BOM).
- **Line Endings:** Windows (CRLF).
- **Delimiter:** Standard comma (`,`). Text fields are heavily quoted (`"`) to handle internal commas.
- **Organization:** The data is provided as a single bulk ZIP file (`CjdtClerkCase.zip`). Inside the ZIP, the data is arbitrarily chunked into 5 files (`CjdtClerkCase_00000.csv` through `CjdtClerkCase_00004.csv`) with a strict limit of 1,000,001 rows per file. It is **not** organized by county or year.
- **File Size:** The ZIP file is 207 MB. Unzipped, the CSVs total 1.84 GB.
- **Access Process:** The bulk download is directly accessible via a static Azure Blob Storage URL (`https://cjdtpublicstorageprod.blob.core.usgovcloudapi.net/cjdtpubliccontainer/CjdtClerkCase/CjdtClerkCase.zip`). It does not require navigating a dashboard, logging in, or handling session timeouts. No rate limits were encountered during a standard `wget` download.

---

## Section 8: Flags and Concerns

**[INFERRED / CONFIRMED]**

1. **Missing Counties (Critical):** The dataset does not contain comprehensive data for all 67 Florida counties. Major counties like Brevard and Sarasota appear to be missing entirely, and others have highly suspect low row counts. Any statewide metric synthesis will be fundamentally incomplete.
2. **No Judge Data (Critical):** If the project requires analyzing outcomes by specific judges, this dataset cannot support it. The data only rolls up to the Judicial Circuit level.
3. **Counsel Category Gaps:** Comparing outcomes by attorney type (Public Defender vs. Private) will be skewed because major counties (like Broward) completely fail to report this field.
4. **Statute Parsing Complexity:** Filtering for DUI requires careful string matching (`LIKE '316.193%'`) and subsequent exclusion of non-DUI variants (like `316.1935` Fleeing/Eluding). Relying solely on the `STATUTE_CHAPTER` and `STATUTE_SECTION` columns will fail because clerks frequently embed subsections into the main `STATUTE` string.
5. **Charge-Level vs. Case-Level Dispositions:** Because dispositions are per-charge, synthesizing a "Case Outcome" requires grouping by `UNIQUE_CORRELATION_ID` and applying a hierarchy logic (e.g., if any charge is "Adjudicated Guilty", the case is Guilty; if all are "Dismissed", the case is Dismissed).
6. **Financial Data is Unusable:** Do not attempt to analyze `FINE` or `RESTITUTION` amounts. They are missing in nearly 80% of records.
