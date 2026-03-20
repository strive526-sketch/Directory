# V5 Working Notes — Comprehensive Amendment Log

**Date:** March 20, 2026
**Status:** Phase 1A data profiling complete. Core differentiator identified. Page architecture reframing in progress.
**Replaces:** Earlier working notes file (March 19). This document is now the canonical supplement to V5.

---

## Part 1: The Core Differentiator — Data Interpretation, Not Data Display

### What We Discovered

The single most important finding from Phase 1A is not a number. It's a pattern.

Duval County reports an 86% county jail rate for DUI convictions. FloridaCourtFile.com publishes this number on their Duval page. A reader sees "86% jail" and panics. But when we examined the underlying sentence length distribution, we found:

- 58.6% of Duval's "jail sentences" are for 1-2 days
- In 85.6% of cases, the defendant's credit time served (the night in booking after arrest) completely covers the sentence
- The judge is retroactively converting the booking stay into the official "jail sentence"
- The defendant does not return to custody after court

Compare Hernando County at 17% jail: median sentence of 60 days, only 3% are 1-2 day entries, 33% are 91+ days. Hernando's 17% means real jail time. Duval's 86% mostly means "we counted the drunk tank."

FCF publishes both numbers identically, with the same template, and the same generic disclaimer. Because they're reading a field and displaying it. They cannot — within their programmatic template model — cross-reference the confinement field against sentence length and credit time served to determine whether a jail rate reflects reality or a coding artifact.

### Why This Is The Differentiator

This is not a one-off anomaly. This pattern will exist in every metric, in every county, in every charge type. Reporting artifacts, clerk coding differences, county-level data entry practices — they're baked into the CJDT dataset. Any platform that displays raw CJDT numbers without interpretation is publishing numbers that range from accurate to actively misleading, with no way for the reader to tell the difference.

**Our competitive position:** We don't display data. We interpret data. We cross-reference fields within the same dataset to validate what a number actually means before presenting it to a reader. When a number is solid, we present it with confidence and sourcing. When a number is ambiguous or potentially artifactual, we disclose that specifically — not with a generic disclaimer, but with an explanation of exactly what might make this number unreliable and why.

This is the Our World in Data model from V5 made concrete. The methodology IS the credibility. But now we have an empirical proof case for why it matters.

### What This Entails Operationally

**For every metric on every page, we need a validation layer:**

1. **Field-level cross-referencing.** Before publishing any confinement rate, cross-check against sentence length distribution and credit time served. Before publishing any fine average, check the distribution for outliers that skew the mean. Before publishing any counsel type comparison, check coverage rates by county and exclude counties below threshold.

2. **Per-county coding pattern identification.** Build a profile for each county's reporting patterns. Which counties code "time served at booking" as County Jail? Which counties have >90% null on certain fields? This becomes a metadata layer that informs how we present every number for that county.

3. **Honest presentation framework.** Three tiers of confidence for displayed statistics:
   - **High confidence:** Cross-references validate. Number means what it appears to mean. Present with source citation and sample size.
   - **Moderate confidence:** Potential coding artifacts or partial data. Present with specific caveat explaining the issue. "This figure may include [specific artifact]. See methodology."
   - **Low confidence / suppressed:** Data too unreliable for the reader to act on. Don't display. Note that data is available but not reliable enough to report.

4. **Methodology documentation per metric, not just per page.** Not a single methodology section at the bottom. Each data point that has caveats gets its caveat inline or immediately adjacent. An LLM extracting one block gets the claim AND the caveat together.

### How This Could Be Implemented

**Option A: Manual editorial review per county per metric.** Run the cross-reference validation queries for each county. Human reviews results. Flags metrics as high/moderate/low confidence. Writes specific caveats where needed. This is the Phase 1 approach — manual, accurate, slow. Produces the editorial decision register.

**Option B: Automated pre-screening with human review.** Build validation scripts that automatically flag: any county where >50% of jail sentences are 1-2 days, any county where credit time served covers >70% of sentences, any metric where the county value is >2 standard deviations from statewide (potential outlier or artifact). Human reviews flagged items only. This is Phase 2 — scalable, but requires initial manual calibration.

**Option C: Composite scoring.** For each metric in each county, compute a "reporting confidence score" from multiple signals (sentence length distribution, credit time served coverage, comparison to similar-sized counties, temporal consistency). Display the score alongside the metric. Fully transparent. This is aspirational — the score itself would need validation.

**Recommended path:** Option A for Phase 1 (DUI, Florida). Build the validation queries, run them for all counties, manually review, encode results. The results become training data for Option B when scaling to additional charge types and states.

### What FCF Cannot Do

FCF's architecture (FastAPI + Jinja2 + ~10 templates, programmatic generation) is optimized for: read field, display field, repeat 4,500 times. To implement the interpretation layer described above, they would need to:

- Write per-county logic that adjusts how metrics are presented based on coding pattern analysis
- Add editorial content that varies by county and metric
- Maintain county-level metadata about reporting practices
- Fundamentally shift from "one template, many pages" to "one template, many conditional presentations with editorial overlays"

This isn't impossible for them, but it runs counter to their lead-gen incentive structure (more pages = more attorney inventory) and their operational model (zero manual labor per page). Every hour spent on editorial interpretation is an hour not spent expanding to the next state. Their Virginia and New York sites confirm they're choosing horizontal expansion over vertical depth.

---

## Part 2: V5 Corrections — What The Data Actually Shows

### Correction 1: DUI Disposition Distribution

**V5 assumed (from overall dataset):** ~63% Guilty, ~22% AW, ~7% Diversion, ~5% Dismissed
**DUI-specific reality (2023-2025):** 93.4% Guilty, 2.1% AW, 1.6% Diversion, 1.7% Dismissed

**Impact:** V5's content inclusion matrix (Section 7) rated AW explanation as HIGH benefit for DUI based on the 22% assumption. For DUI, AW is a minor footnote at 2.1%. The entire V5 framing around "realistic outcomes" assumed meaningful disposition variance — some get convicted, some get AW, some get dismissed. DUI reality is: you're almost certainly getting convicted, and the meaningful variance is in what the sentence looks like.

**However:** AW is a massive story for other charge types. Hit and Run: 43.6% AW. Marijuana Possession: 43.1% AW. Battery: 21.2% AW. Moving Traffic: 37.7% AW. For the majority of charge types this platform will cover, AW explanation is among the highest-value content elements. V5 was right about the platform, just wrong about DUI specifically.

**Action:** Information sequencing for DUI pages leads with sentencing reality, not disposition variance. For non-DUI charge types, disposition variance (especially AW) moves to position 1-2 in the sequence.

### Correction 2: County Coverage

**V5 stated (Section 12):** 56 of 67 counties. 4 missing: Brevard, Charlotte, Okaloosa, Sarasota.
**Reality:** All 67 counties present in dataset. Sarasota alone has 5,818 DUI records. Some small counties have very low volume indicating partial reporting, but none are absent.

**Impact:** The "statewide with gaps" framing should be replaced by "statewide with variable reporting depth." Small county caveat methodology applies (Section 15 of V5 still valid) but the coverage gap disclosure changes.

### Correction 3: DUI Record Count

**V5 estimated:** ~340,000-350,000 DUI records
**Reality:** ~141,000-144,600 using statute filter (316.193% excluding .1935, .1939). The higher V5 estimate likely included related statutes or used FCIC_Category which captures misclassified records.
**2023-2025 subset:** ~62,558 convicted cases (the directly comparable window to FCF)

**Impact:** Sample sizes still robust statewide and for high-volume counties. Low-volume counties need more careful threshold handling than V5 assumed.

### Correction 4: PERSON_ID

**V5 flagged as blocker:** Is PERSON_ID reliable for cross-county individual tracking?
**Result:** Completely broken. 0% cross-county linkage. IDs reset per county.
**Rescue:** MDM_PERSON_ID shows 4.57% cross-county linkage with 87-95% demographic consistency. Viable as lower bound for repeat offender identification with methodology disclosure.

**Impact:** "First offense" situational pages are viable but require honest framing: "First offense defined as no prior DUI charge for same individual identified via FDLE's master data matching algorithm in the CJDT dataset (2018-present). This represents a lower bound — individuals with prior DUIs in other counties or before 2018 may not be identified. False negatives are likely; false positives are rare."

### Correction 5: SAO Cross-Reference

**V5 planned (Section 11):** SAO dataset linkable via UNIQUE_CORRELATION_ID for case-level prosecutorial funnel analysis.
**Reality:** Zero linkage. SAO and Clerk systems generate UNIQUE_CORRELATION_IDs independently. 0 matches out of millions of records on both sides.

**Impact:** Case-level prosecutorial funnel is dead. The multi-source cross-referencing thesis from V5 Section 11 loses its primary mechanism for case-level linkage. However:
- SAO data is valuable standalone: county-level filing rates show real variance (Orange drops 35% of DUI cases, Flagler drops 2.5%)
- Aggregate cross-referencing (total SAO DUI cases vs total Clerk DUI cases per county per year) is feasible
- Other CJDT portal datasets (County Detention, DOC) likely have the same linkage problem — worth verifying but should be assumed broken until proven otherwise

### Correction 6: Temporal Ramp-Up

**V5 assumed:** Data from ~2018 to present, usable throughout.
**Reality:** 2018 had only 3,186 DUI records. Volume didn't stabilize at ~22,000/year until 2022. Counties onboarded gradually.

**Impact:** Minimum defensible trailing window starts 2021 for trend analysis. Any window including 2018-2020 reflects incomplete county onboarding, not actual DUI trends. The 2023-2025 window FCF uses is a defensible choice. We should use the same or similar for reader-facing statistics, with full historical range available on Tier 3 synthesis pages with the ramp-up disclosed.

### Correction 7: Sentencing Variance Is The Real Story (For DUI)

**V5 framed disposition variance as the core data story.**
**Reality for DUI:** Disposition is flat (93% guilty). Sentencing variance is enormous:
- Confinement rates: 4.4% (Escambia) to 87.6% (Marion) — but this is BEFORE the booking-artifact correction
- Court costs: $270 (Martin) to $2,082 (Lee)
- Max term: 2 days median (Duval) to 120 days (Pasco)
- Probation: Flat at 365 days everywhere (no story)

**CRITICAL CAVEAT (from Query 2 findings):** The confinement rate variance is partially artifactual. Duval's 86% is mostly booking credit. The real variance — after correcting for booking artifacts — is still meaningful but needs quantification across all counties. This is the pending analysis.

**Impact:** The charge page doesn't lead with "here's the conviction rate." It leads with "conviction is near-certain — here's what the sentence actually looks like in your county" and then presents the sentencing data WITH the interpretation layer that explains what it really means.

---

## Part 3: CourtFile LLC — Updated Competitive Intelligence

### Multi-State Presence [CONFIRMED]

CourtFile LLC operates three sites:
- **VirginiaCourtFile.com** — oldest, ~3 weeks older than Florida
- **FloridaCourtFile.com** — launched March 8, 2026
- **NewYorkCourtFile.com** — launch date unconfirmed

All show top organic rankings. All show zero AI Overview citations. Virginia's longer timeline with same result reinforces sandbox interpretation.

### Tech Stack [CONFIRMED]

- FastAPI (Python), Jinja2 server-side templates, custom CSS (42KB), Railway hosting
- Database serving 1,690,714 records
- Internal API confirmed (endpoints like /api/v1/stats?charge=dui&county=orange)
- ~10 template files generating 4,500+ pages per state
- 0.07 second page loads
- Monthly data refresh via automated pipeline

### Data Validation Against FCF [CONFIRMED]

We validated our computed numbers against FCF's published numbers for Hernando, Duval, Escambia, and Marion counties. Results: financial metrics match within dollars. Confinement rates match within 1-3%. They are reading the same CJDT data with the same basic methodology. Minor discrepancies likely from date cutoff differences or null handling.

### FCF's Methodology Gaps (Our Opportunities)

1. **Sentence length calculation:** FCF reports "average sentence 1.3 months" statewide. Raw MAXIMUM_TERM_DURATION_DAYS computes to 4.15 months. FCF is likely computing something different (actual time served vs. maximum term). Neither number is wrong but FCF doesn't disclose which they're using or why. We can show both with explanation.

2. **Confinement rate without interpretation:** FCF shows Duval at 86% jail. This is technically correct but misleading. 58.6% of those are 1-2 day booking credits. FCF has no mechanism to interpret this — their template reads a field and displays it.

3. **No cross-metric validation:** FCF doesn't cross-reference SENTENCE_CONFINEMENT against MAXIMUM_TERM_DURATION_DAYS or CREDIT_TIME_SERVED. They treat each field as independent. We treat them as a system that validates or invalidates each other.

4. **Generic disclaimers vs specific methodology:** FCF has a one-size-fits-all disclaimer. We document methodology per metric with specific caveats per county where reporting artifacts exist.

### FCF Data Presentation Audit [CONFIRMED]

Direct inspection of FCF's published pages for Duval, Pinellas, Orange, Miami-Dade, and their methodology/about pages. Findings:

**What FCF shows:**
- Duval: 86% jail, avg sentence 1.2 months, median 2 days. No explanation connecting these contradictory facts.
- Orange: 91.6% jail, 75th percentile 2 days (meaning 75%+ of jail sentences are ≤2 days). No caveat.
- Miami-Dade: 237 cases presented identically to Pinellas's 7,577. No data completeness warning.
- Pinellas: 44% jail, median 2 months. The one county where their presentation happens to match reality.

**What FCF does NOT disclose (confirmed absent from all pages, methodology, guides, and about page):**
- Credit time served — not mentioned anywhere on the site
- Booking artifact patterns — not acknowledged
- Miami-Dade coverage gap — not flagged
- Sentence length vs time served distinction — not explained
- CJDT data submission variability — not mentioned
- Sentinel values in CREDIT_TIME_SERVED — not addressed

**FCF's methodology definition:** "Jail = sentence of 1-365 days." By this definition, a 1-day booking credit IS jail. Technically defensible. Practically misleading.

**FCF's quality standard:** "Pages with fewer than 10 cases are excluded from search engine indexing." That's the entire quality gate. No per-county data quality assessment. No cross-field validation.

**Our advantage is now empirically documented.** For every issue we've identified — booking artifacts, Miami-Dade gap, CTS coverage, sentence length interpretation — FCF publishes raw numbers without context. We interpret, cross-reference, and disclose. The difference is visible on every page, not just in methodology sections.

### Updated Competitive Framing

FCF is a legitimate competitor executing well on a programmatic model. They will likely receive AI citations eventually (sandbox timing, not structural failure). They are expanding state-by-state faster than we can. Their lead-gen model is proven.

Our differentiation is not "they're worse." It's "we do something they structurally can't within their model." They display data. We interpret data. They show what the database says. We show what the database means. Every misleading number they publish without context is a concrete example of why interpretation matters. We frame this as "we go further" not "they're wrong."

The FCF audit gives us concrete proof points: same data source, same numbers, radically different presentation quality. An LLM evaluating citation candidates can compare our Duval page (connecting the 86% jail rate to the 2-day median and CTS coverage) against FCF's (displaying both facts without connecting them) and make a clear judgment about which source demonstrates deeper understanding of the data.

---

## Part 4: Reader Intent Reframe

### V5 Was Already Right (We Drifted)

V5 Section 8 (Information Sequencing) and Section 7 (Reader Models) describe exactly the right approach: the stressed person at 2 AM, scanning on mobile, looking for anchors. BLUF first, realistic outcomes second, "what makes it beatable" third. Data serves the reader's questions — it doesn't lead.

During Phase 1A analysis, we drifted toward data-first thinking: "look at this variance, this should be the page." The variance is real and valuable, but nobody searches for "DUI sentencing variance by county." They search:

**Hours 0-24 (crisis):**
- "how long do you stay in jail for DUI Florida"
- "DUI bail [county]"
- "first DUI arrest what happens now"
- "will I lose my license DUI Florida"
- "do I need a lawyer for DUI"

**Days 2-14 (pre-arraignment):**
- "first DUI Florida penalties"
- "DUI arraignment what to expect"
- "can DUI be dismissed Florida"
- "DUI lawyer [city/county]"
- "DUI diversion program [county]"

**Weeks/months (case in progress):**
- "DUI plea deal Florida"
- "DUI reduced to reckless driving Florida"
- "how long DUI probation Florida"

The data answers these questions. "How long do you stay in jail for DUI" → our data shows that in most counties, the booking night IS the jail time. That's enormously more useful than "up to 6 months" (statutory maximum that every attorney site publishes) or "86% jail rate" (FCF's raw number that terrifies the reader unnecessarily).

### What This Means For Page Design

Pages are organized by what people search and what they need, not by what the data can show. The data makes the answers trustworthy and specific. It doesn't determine the structure.

The charge page for "DUI in Florida" answers reader questions in order of urgency, with data providing the evidence for each answer. The county interactive element lets them drill into their specific situation. The sentencing variance IS on the page — but it's not the headline. It's the supporting evidence for "here's what will realistically happen to you in your county."

This aligns with V5's Priority Stack: Reader Benefit first, LLM readability second, net-new third. The data is what makes our answers better than every other site's answers. But the reader came for the answer, not the data.

---

## Part 5: Data Truthfulness Framework

### The Disclosure Principle

Every statistic published on the platform comes from records reported by county clerks to FDLE under Florida Statute 900.05. This is mandatory administrative reporting, not independently verified case outcomes. The data represents what was officially reported.

This matters because:
- Clerk coding practices vary by county (the Duval booking-credit pattern)
- Some fields have systematic gaps (COUNSEL_CATEGORY missing for Broward and Miami-Dade)
- The dataset captures filing-through-sentencing but not arrest, not administrative license action, not post-conviction compliance
- "Not Available" is a data entry choice, not proof of absence

### Per-Metric Disclosure Template

For each metric displayed, we need to answer:
1. **What field(s) does this come from?** (Not visible to reader, documented in methodology)
2. **What does this field actually measure?** (Plain language)
3. **Are there known coding artifacts for this county?** (If yes, specific caveat)
4. **What is the sample size?** (Always displayed)
5. **What time period?** (Always displayed)
6. **What's excluded and why?** (Specific to this metric)

### Example Application: Jail Rate

**Without interpretation (FCF approach):**
"86% of DUI convictions in Duval County result in county jail."

**With interpretation (our approach):**
"In Duval County, 86% of DUI convictions include a recorded jail component. However, in the majority of these cases (approximately 59%), the recorded sentence is 1-2 days — typically reflecting the time already served at booking after arrest, not an additional jail sentence imposed by the court. Only about [X]% of Duval County DUI defendants receive a jail sentence requiring them to return to custody. Based on [N] cases, 2023-2025, FDLE CJDT Clerk Case data."

The second version is longer. It's also the only version that actually helps the reader understand what will happen to them. Reader Benefit wins over brevity.

---

## Part 6: Charge Type Expansion Landscape

### Key Discovery: AW Is The Platform Story

DUI is atypical. Its 2.1% AW rate is the lowest of any major charge type. Across the platform:

| Charge Type | AW Rate | Significance |
|---|---|---|
| Hit and Run | 43.6% | AW is the most common outcome |
| Marijuana Possession | 43.1% | AW is the most common outcome |
| Moving Traffic | 37.7% | AW exceeds guilty rate |
| Nonmoving Traffic | 34.6% | AW exceeds guilty rate |
| Damage Property | 22.6% | AW is a primary outcome |
| Battery | 21.2% | AW is a primary outcome |
| Larceny | 20.2% | AW is a primary outcome |
| Drug Possession | 20.1% | AW is a primary outcome |
| Resist Officer | 19.6% | AW is near-primary |
| DUI | 2.1% | AW is negligible |

For most of the charge types this platform will cover, the AW explanation — what it means, how it differs from conviction, what the practical implications are — is among the highest-value content we can provide. This is content that every reader needs and no competitor provides clearly.

### Expansion Readiness Assessment

**Tier 1 (Ready now, same pipeline):**
- Drug Possession (54K cases 2023-2025, 50+ counties >100 cases, 20.1% AW rate — strong reader need for AW explanation)
- Battery (73K cases, 54 counties, 21.2% AW, 18.3% diversion — diversion is also a major story)

**Tier 2 (Ready but messy statute mapping):**
- Larceny (110K cases but 101 statute strings — need to define inclusion/exclusion)
- Trespassing (63K cases, 38 statute strings)
- Resist Officer (49K cases, 34 statute strings)

**Tier 3 (Needs investigation):**
- Moving Traffic Violation (298K cases but extremely broad — may need to split into sub-categories)
- Drug Equipment Possession (52K cases, typically co-occurring with Drug Possession — may not justify standalone page)

**Universal challenge:** Statute mapping is messy for all categories except County/Municipal Ordinance. For each new charge type, we need a documented decision: use FCIC_Category (cleaner, but has clerk misclassification noise) or statute wildcard (more precise, but has gaps). This is a methodological decision that gets logged in the editorial decision register per charge type.

---

## Part 6B: County Jail Classification Framework [CONFIRMED]

### The Three Patterns

Analysis of sentence length distribution and credit time served for the top 10 DUI counties plus Marion reveals three distinct patterns. This is now the foundational framework for how confinement rates are presented on every page.

**BOOKING ARTIFACT** — High jail rate is misleading. Median sentence ≤2 days. CTS covers sentence in ≥70% of cases. The "jail sentence" is retroactive credit for the arrest booking stay.
- Duval: 86% jail rate, but 58.6% are 1-2 day sentences, 85.6% fully covered by CTS

**REAL JAIL** — Jail rate reflects actual post-conviction incarceration. Median sentence >7 days. CTS covers sentence in <50% of cases. Defendant returns to custody.
- Hillsborough: 17.6% jail rate, median 45 days, CTS covers only 29.9%
- Pinellas: 41.8% jail rate, median 60 days, CTS covers only 28.9%
- Broward: 13.7% jail rate, median 60 days, CTS covers only 25.0%
- Collier: 30.2% jail rate, median 45 days, CTS covers only 43.2%

**MIXED** — Combination of booking credits and real sentences. Requires nuanced presentation.
- Marion: 85% jail, median 6 days, 71.1% CTS coverage (leans artifact)
- Palm Beach: 46% jail, median 30 days, 56.3% CTS coverage
- Lee: 37.7% jail, median 20 days, 57.0% CTS coverage
- Bay: 27.5% jail, median 30 days, 66.4% CTS coverage
- Sarasota: 35.5% jail, median 30 days, 86.1% CTS coverage

**DATA ANOMALY:**
- Polk: median CTS of 999 days is a sentinel value (likely "not applicable"). Must be excluded from CTS-based analysis. Classify Polk on sentence length distribution only (median 80 days, only 0.2% are 1-2 day — likely Real Jail pattern once sentinel values are excluded).

### Key Insight: Pinellas at 42% Is Scarier Than Duval at 86%

This is the single clearest proof of why interpretation matters. A reader comparing counties on FCF sees Duval at 86% jail and Pinellas at 42% and concludes Duval is far harsher. Reality is inverted. Pinellas's 42% means a real 60-day median sentence with only 29% covered by time served. Duval's 86% mostly means "we credited your booking night." Publishing raw percentages without this context actively harms the reader's ability to make informed decisions.

### Presentation Templates By Classification

**Booking Artifact counties:**
"While [X]% of DUI convictions in [County] are recorded with a jail component, the majority reflect credit for time already served at initial booking (median recorded sentence: [N] days). In most cases, defendants do not return to custody after their court appearance."

**Real Jail counties:**
"[X]% of DUI convictions in [County] include a jail sentence. The median sentence is [N] days, and in most cases defendants serve this time after their court date."

**Mixed counties:**
"[X]% of DUI convictions in [County] include a jail sentence. Sentences vary — approximately [N]% are short-term booking credit, while the remainder average [N] days. In roughly [half/most] of cases, pre-trial time served covers the full sentence."

These templates are dynamically applied per county based on classification criteria. They require no manual writing per county — the classification drives template selection, the numbers populate from the data. This is editorially sound AND scalable.

### Complete Classification Results [CONFIRMED]

Full statewide analysis completed for all counties with ≥50 DUI jail cases (2023-2025). 42 counties classified:

**BOOKING ARTIFACT (5 counties):** Duval, Osceola, Orange, Leon, Baker
- These counties' jail rates are misleading. The "sentence" is retroactive booking credit.
- Notably includes two major metros: Duval (Jacksonville) and Orange (Orlando)
- Orange is the most extreme: 77.1% of jail sentences are 1-2 days, 96.4% covered by CTS

**REAL JAIL (25 counties):** Pinellas, Hillsborough, Polk*, Collier, St. Lucie, Martin, Indian River, Pasco, Charlotte, Broward, St. Johns, Santa Rosa, Citrus, Manatee, Alachua, Seminole, Lake, Okaloosa, Okeechobee, Sumter, Escambia, Highlands, Hardee, Jackson, Nassau
- Median sentences range from 22 days (Hardee) to 114 days (Sumter)
- Most cluster around 30-90 days
- Pasco (90 days median, 10.1% CTS) and Okaloosa (75 days, 0.0% CTS) are the harshest
- *Polk classified on sentence length only due to CTS sentinel value contamination (69.2% of records show 999)

**MIXED (12 counties):** Palm Beach, Marion, Lee, Volusia, Sarasota, Bay, Clay, Walton, Monroe, Putnam, Bradford, Hernando
- Varying combinations of booking credit and real sentences
- Some lean artifact (Marion, Clay, Putnam, Bradford — high % 1-2 day, high CTS coverage)
- Some lean real (Sarasota, Hernando — longer medians but high CTS coverage suggesting pre-trial plea deals)

**Key finding:** Most of Florida is Real Jail for DUI. 25 of 42 classified counties. The booking artifact pattern is the exception (5 counties), not the rule. The honest answer to "am I going to jail" in most Florida counties is: if convicted, there's a meaningful probability of real jail time, typically 30-90 days.

**Remaining:** ~25 counties with <50 jail cases need threshold handling (either show rate with "insufficient data to characterize" caveat, or suppress). Analysis queued.

### Low-Volume County Handling [CONFIRMED]

23 counties fall below the ≥50 jail case threshold. Complete threshold logic for the interactive element:

**≥50 jail cases** → Show rate + classification pattern (Booking Artifact / Real Jail / Mixed template)
**10-49 jail cases** → Show rate with caveat: "X% include a jail component — insufficient data to characterize typical sentence length"
**<10 jail cases or <50 total convictions** → Suppress jail metric entirely. Show only: "Insufficient DUI case data available for [County]."

Counties suppressed entirely (jail metric): Glades (24 convictions), Union (19), Gadsden (14), Lafayette (11), Liberty (10), Taylor (6).

### CRITICAL: Miami-Dade Data Gap [CONFIRMED]

Miami-Dade County — population 2.7 million, Florida's most populous county — shows only 167 DUI convictions in the 2023-2025 dataset. For comparison, Hillsborough (population 1.5M) has 13,981. Miami-Dade's figure is almost certainly a data submission failure, not reality.

Combined with Broward's 0% COUNSEL_CATEGORY coverage, the two largest South Florida counties (combined ~4.5M population, ~20% of Florida) are either absent or compromised on key metrics.

**Implications:**
- All "statewide" statistics must disclose that Miami-Dade appears to be severely underreported
- Miami-Dade should be excluded from statewide calculations with disclosure, OR included with prominent caveat
- The interactive element for Miami-Dade should show the data we have with explicit warning: "Miami-Dade County's CJDT data appears substantially incomplete. Only 167 DUI dispositions were reported for 2023-2025 — far below what population and arrest data would predict. Statistics for this county may not reflect actual outcomes."
- This gap is itself a publishable Tier 3/4 finding about Florida's data transparency system

**This reinforces the Data Truthfulness pillar.** Any platform that publishes Miami-Dade DUI statistics from CJDT without this disclosure is misleading readers. FCF has Miami-Dade pages populated from this same thin data. We disclose. They don't.

---

## Part 7: What's Still Pending

### Analyses In Progress

1. ~~**Top 10 county jail sentence distribution**~~ COMPLETE. See Part 6B above.

2. ~~**Marion deep-dive**~~ COMPLETE. Marion is Mixed (leans artifact). 42% of sentences are 1-2 days, median 6 days, but 34.4% are 31+ days suggesting some real sentences mixed in.

### Analyses Needed (Not Yet Queued)

3. **Diversion program mapping** — Which counties have formal DUI diversion programs (Hillsborough RIDR, Pinellas DROP, etc.)? Does our Pre-Trial Diversion field correlate with known program counties? This is high reader-benefit content: "Your county has a diversion program that may allow you to avoid a DUI conviction."

4. **Temporal trends in sentencing** — Are counties getting harsher or more lenient over the 2021-2025 window? Post-Trenton's Law (October 2025) shift detectable in 2025 Q4 data?

5. **Attorney type outcomes with severity control** — For counties with good COUNSEL_CATEGORY data, does the public defender vs private attorney outcome difference survive when controlling for charge Level/Degree? This is the confounding control V5 requires.

6. **UCR arrest data download and aggregate funnel** — FDLE publishes DUI arrest counts by county in Excel. Cross-referencing total arrests with our Clerk case counts gives the arrest-to-court pipeline at aggregate level. "X arrests in [county], Y cases filed, Z convicted."

7. **Search demand validation** — Before building pages, validate that the intent-driven queries identified in Part 4 have actual volume. This is keyword research but oriented around user journey stages, not ranking targets.

### Decisions Not Yet Made

- Trailing window for reader-facing statistics (2023-2025 matches FCF, 2021-2025 gives more data, 2022-2025 avoids the worst of the ramp-up)
- Sample size thresholds for county-level display (calibrate from actual volatility, V5 Section 15 framework still applies)
- Which counties qualify for standalone pages (V5's three conditions, now with the additional requirement that we've validated their data for coding artifacts)
- Site architecture and tech stack (not needed until page content is defined)
- Domain and branding (not needed yet)

---

## Part 8: Updated Principles (Additions to V5 Section 24)

**25. Raw data display is not data journalism.** A field value is not a finding. Cross-referencing fields to determine what a number actually means — and disclosing when it doesn't mean what it appears to mean — is the minimum standard.

**26. Coding artifacts are county-specific.** The same field can mean different things in different counties depending on clerk practices. Every metric needs per-county validation before publication. Generic statewide methodology is insufficient.

**27. The interpretation layer is the moat.** Schema is infrastructure. Data is commodity (FCF has it). Interpretation — determining what data means, not just what data says — is the editorial judgment that can't be programmatically replicated.

**28. Pages serve the reader's journey, not the data's structure.** People search by crisis stage, not by statistical category. Data answers their questions; it doesn't organize the page.

**29. AW is a platform-wide story, not a DUI story.** Adjudication Withheld is a primary outcome for most charge types and a negligible one for DUI. Content strategy must account for per-charge-type variation in which data elements are highest reader benefit.

**30. Competitor validation is a tool, not a goal.** FCF's published numbers cross-check our methodology. Agreement confirms we're reading the data correctly. It does not confirm the data reflects reality. Ground truth requires interpretation or Tier C contributor validation.

---

## Part 9: Net-New Assessment — What Clears The Reader Benefit Gate

### The Filter

Having data is not the same as having useful data. Each potential net-new element must answer: does this genuinely change how a person charged with DUI thinks, feels, plans, or acts? If it's just interesting, it doesn't go on the page.

### PASSES Reader Benefit Gate

**1. County-Level Total Financial Burden [CONFIRMED FEASIBLE]**

80.1% of DUI convictions have both FINE and COURT_COST populated. Data is robust for most major counties.

*Reader question it answers:* "How much is this going to cost me?"

*Why it matters:* Every attorney site quotes the statutory range ($500-$1,000). The actual median court-imposed total in Escambia is $2,912. In Hillsborough it's $931. The person budgeting based on statutory ranges will be blindsided. This is directly actionable — they can plan financially.

*How to present:* County-specific median total (fines + court costs) with framing: "This reflects court-imposed fines and costs only. Additional costs typically include DUI school (~$350), license reinstatement (~$275), and substantially increased insurance premiums."

*Data gaps:* Lee County and Broward show 0% population on financial fields. Must be suppressed with disclosure, same pattern as other data gaps.

Key variance: Hillsborough $931 → Escambia $2,912 → Indian River $2,846 → St. Lucie $2,741. Enormous spread.

**2. County-Level Non-Conviction Pathways [CONFIRMED FEASIBLE]**

*Reader question it answers:* "Can this be reduced or dismissed?"

*Why it matters:* Not as a "your odds" calculator — that would be irresponsible. But the data shows county-specific pathways that the reader needs to know exist. Orange County has a 40.9% non-conviction rate driven by 28.7% diversion. Collier has 0.7%. The person in Orange County needs to know that diversion pathway exists and is commonly used. The person in Collier needs calibrated expectations.

*How to present:* "In [County], [X]% of DUI cases resulted in an outcome other than conviction: [Y]% through diversion programs, [Z]% dismissed, [W]% acquitted." Framed as informational context, not predictive. With caveat: "Individual outcomes depend on case circumstances, criminal history, and legal representation."

Key variance: Orange 40.9% non-conviction vs Collier 0.7%. Orange's 28.7% diversion rate likely reflects a formal program — worth researching which counties have specific diversion programs to layer in that context.

**3. Refusal Outcome Context [CONFIRMED FEASIBLE]**

11,464 records for statute 316.1939. 63.2% co-occur with standard DUI charge.

*Reader question it answers:* "I refused the breathalyzer — did I screw myself?"

*Why it matters:* Refusal is a major source of panic. The data shows refusal charges are often resolved as part of plea negotiations on the main DUI charge. The overall conviction rate is similar to standard DUI, but the resolution pattern is different. This helps the reader understand what their attorney is likely negotiating.

*How to present:* As a section on the DUI charge page or as a standalone "DUI Refusal in Florida" situational page. "Breathalyzer refusal charges (316.1939) co-occur with DUI charges in 63% of cases. In many instances, the refusal charge is resolved as part of plea negotiations on the primary DUI charge."

### DOES NOT PASS Reader Benefit Gate

**Charge Stacking Metric** — Average charges per case varies from 1.05 (Orange) to 2.27 (Volusia). Knowing the count doesn't help the reader plan or act. The *types* of co-occurring charges (which we already have) are useful. The count isn't. Skip.

**Timeline to Resolution** — Dead anyway (no filing date in data), but even if we had it, "average DUI case takes X months" is useful only at a general level. Without the filing date, we can't build this.

### NOT AVAILABLE (Honest Gaps)

These are questions readers ask that we cannot answer from CJDT data. Disclosing this honestly is better than not addressing it:

- **BAC-to-outcome correlation** — the #1 searched DUI data question. Not in CJDT. Florida breath test records may exist at FDLE but no bulk portal.
- **Judge-level outcome variance** — only Judicial Circuit in data, not individual judges
- **Pre-trial detention impact on outcomes** — can't link jail booking data to court outcomes
- **Actual time served vs sentenced** — CTS field is our best proxy but has sentinel values and gaps
- **Insurance cost impact** — not in any government dataset
- **Time from arrest to resolution** — no arrest or filing date in Clerk data
