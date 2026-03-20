# Project Handoff Report — Legal Data Synthesis Platform

**Date:** March 20, 2026
**Version:** 1.0
**Status:** Phase 1A data exploration complete. Page architecture defined. Build phase not started.

---

## How To Use This Document

This is the entry point. Read this first. It tells you what the project is, what's been done, what hasn't, and where to find everything.

**You do NOT need to read every companion document for every task.** This handoff tells you which documents are relevant to which types of work. Read only what you need for the task at hand.

---

## Companion Documents (In Priority Order)

| Document | What It Contains | When To Read It |
|---|---|---|
| **V5 Checkpoint** (`legal-data-platform-checkpoint-v5.md`) | Full project architecture: terminal objective, four pillars, pipeline, page types, schema strategy, principles, risk registry. The governing document. | Read Sections 1-3 (objective, pillars, constraints) for any strategic work. Read specific sections as referenced by other documents. |
| **V5 Working Notes** (`v5-working-notes-comprehensive.md`) | All Phase 1A findings, V5 corrections, competitive intelligence, data truthfulness framework, jail classification system, net-new assessment, watchlist items. The empirical reality layer. | Read for any data-related work, content work, or competitive positioning. This is where the actual numbers and validated findings live. |
| **DUI Page Architecture** (`dui-florida-page-architecture.md`) | Section-by-section content map for every DUI Florida page. What goes on each page, why, what data backs it. | Read when building any DUI page or when designing pages for a new charge type (as reference template). |
| **Charge Page Framework** (`charge-page-framework.md`) | The generalizable layer: block library, situational page discovery process, charge type profiles, transferability analysis. | Read when expanding to new charge types (Battery, Drug Possession, etc.) or when designing the platform-wide content architecture. |
| **V5 Supplement** (`v5-supplement-competitive-and-scaling.md`) | Competitive analysis, scaling principles, building priorities. Written by a separate LLM — mostly accurate but contains some overconfident competitive framing. See Working Notes Part 10 for calibration. | Skim for competitive context. Cross-check claims against Working Notes. |

---

## What This Project Is

A data synthesis platform that turns fragmented public court data into genuinely useful, reader-benefit-driven content about criminal case outcomes. The legal vertical (starting with Florida DUI) is the first instantiation. The terminal objective is canonical citation authority — being the source AI systems cite for regulatory outcome data.

**The core differentiator (validated in Phase 1A):** We don't display data. We interpret data. We cross-reference fields within the same dataset to determine what numbers actually mean before presenting them to readers, and we disclose honestly when numbers are ambiguous or potentially misleading. This is the thing our primary competitor (FloridaCourtFile.com) structurally cannot do within their programmatic template model.

**The proof case:** Duval County reports an 86% jail rate for DUI. FCF publishes this number. But 59% of those "jail sentences" are 1-2 days (booking credit), and 86% are fully covered by credit time served. The defendant doesn't go back to jail. Meanwhile Pinellas at 42% jail has a median sentence of 60 days with only 29% covered by CTS — real jail time. FCF presents both identically. We interpret both accurately. This pattern is confirmed across 42 Florida counties.

---

## What's Been Done

### Data Acquisition & Profiling ✓

- FDLE CJDT Clerk Case dataset downloaded and profiled (4,092,481 records, 55 columns)
- DUI subset extracted via statute filter 316.193% (excluding .1935 and .1939) — ~144,600 records total, ~62,558 convicted cases 2023-2025
- Full column-by-column profiling with confidence tiers (high/moderate/unusable)
- SAO Case Reports dataset downloaded and profiled (2,942,033 records)

### Validation Checks ✓

- **PERSON_ID:** Broken for cross-county tracking (0% cross-county linkage). Dead for statewide individual tracking.
- **MDM_PERSON_ID:** Partially viable (4.57% cross-county, 87-95% demographic consistency). Usable as lower bound for repeat offender identification with methodology disclosure.
- **UNIQUE_CORRELATION_ID cross-dataset linkage:** Dead. Zero matches between SAO and Clerk datasets. Case-level prosecutorial funnel is not buildable.
- **Charge vs case level divergence:** <0.5 percentage points. Low-stakes framing choice. Case-level recommended.
- **County coverage:** All 67 counties present (V5 said 56 — corrected). Variable reporting depth.
- **Miami-Dade:** Near-absent for misdemeanor DUI (167 records in 3 years for a 2.7M population county). Submits felony cases normally. Data submission failure specific to misdemeanor DUI.
- **Broward:** 0% COUNSEL_CATEGORY coverage, financial fields also 0%.

### DUI-Specific Analysis ✓

- **Disposition:** 93.4% guilty, 2.1% AW, 1.6% diversion, 1.7% dismissed (radically different from overall dataset at 63% guilty, 21% AW)
- **Jail classification:** 42 counties classified into Booking Artifact (5), Real Jail (25), Mixed (12). Full metadata table with sentence length distributions and CTS coverage.
- **Financial burden:** Median statewide $1,468 (fines + court costs combined). Range: $931 (Hillsborough) to $2,912 (Escambia). 80% field coverage.
- **Non-conviction pathways:** Massive county variance. Orange 40.9% non-conviction (28.7% diversion), Collier 0.7%.
- **Refusal (316.1939):** 11,464 records, 63% co-occur with standard DUI, often resolved in plea negotiations.
- **Co-occurrence:** Top co-charges identified (316.1939, 322.34, 843.02, county ordinance violations).
- **Temporal:** Data stabilizes 2021+. 2018-2020 reflects county onboarding, not DUI trends. 2023-2025 is the defensible reader-facing window.
- **Low-volume counties:** 23 counties below classification threshold. Threshold logic defined (≥50 jail cases = full display, 10-49 = rate with caveat, <10 = suppress).

### Competitive Intelligence ✓

- **FCF validated as same data source.** Our numbers match theirs within dollars on financials, within 1-3% on confinement rates. Same CJDT data, same basic methodology.
- **FCF audit completed.** Inspected Duval, Pinellas, Orange, Miami-Dade, and methodology pages. Confirmed: zero mention of credit time served, booking artifacts, Miami-Dade gap, or sentence length interpretation anywhere on their site.
- **FCF multi-state:** Virginia, New York, Florida. All zero AI citations. Sandbox timing, not structural failure.
- **FCF tech stack:** FastAPI, Jinja2, Railway, ~10 templates, 0.07s loads, internal API confirmed.

### Expansion Profiling ✓

- Top 15 charge types profiled at surface level (disposition, volume, AW rate, statute mapping complexity, counsel coverage)
- Battery (73K cases, 21% AW, 18% diversion) and Drug Possession (54K, 20% AW) identified as next candidates
- AW confirmed as the platform-wide story (>10% for 13 of 15 charge types, >43% for marijuana and hit-and-run)
- Statute mapping universally messy (Larceny: 101 strings, Battery: 31, Drug Possession: 25)

### Architecture & Framework ✓

- DUI page architecture defined: 7 primary pages + conditional county pages + related statute infrastructure
- Block library defined: 11 modular content components with data sources, availability, and charge-type variation notes
- Situational page discovery process formalized: 4-step method (identify dimensions → assess filterability → map block assembly → existence test)
- Template transferability mapped from DUI to Battery

---

## What Has NOT Been Done

### Data Verification ⚠️

**CRITICAL: All numbers from Phase 1A are single-source, single-run outputs from Manus (an AI agent). None have been independently verified.** The data exploration was designed to understand what's available and what's viable, not to produce publication-ready statistics. Before any number appears on a published page:

- Raw queries must be re-run in a controlled, reproducible environment (direct database queries, not AI agent)
- Key findings (jail classification, financial burden, non-conviction pathways) need independent verification
- Edge cases in filtering logic need review (how exactly does the statute filter handle subsection variations?)
- County-level numbers for any county that will display data need individual spot-checking
- The booking artifact classification criteria (Median Max Term ≤2 days AND CTS ≥70%) need validation — are the thresholds right? Are there edge cases?

This is not a "nice to have." Publishing unverified statistics on a platform whose entire value proposition is data accuracy would be a credibility-destroying mistake.

### Content Creation

- No page content has been written. Architecture is defined, content is not.
- No BLUF text drafted for any page
- No editorial framing written for the interpretation layer (the Duval/Pinellas comparison text exists in working notes as examples, not as publishable content)
- No methodology page written
- No about page / credibility signals written

### Technical Build

- No site architecture decided (static, server-rendered, hybrid)
- No tech stack chosen
- No domain registered
- No schema structure implemented or tested
- **Schema density not validated against Rich Results Test** — this is a potential blocker (see Working Notes Part 10)
- No interactive county element prototyped
- No design work

### Second Charge Type

- Battery profiling prompt not yet written (pipeline is defined, execution hasn't started)
- No booking artifact analysis for non-DUI charges
- DV indicator field not validated for Battery-specific use
- No statute mapping decision made for Battery (FCIC category vs statute wildcard)

### Research Gaps

- Diversion programs by county not mapped (we know RIDR in Hillsborough, DROP in Pinellas — that's it)
- Search demand not validated (crisis-stage query model is first-principles, not keyword data)
- DUI-with-injury subsection filtering not tested (316.193(3)(c) via STATUTE_SUBSECTION field)
- UCR arrest data not downloaded (aggregate arrest counts for funnel top)
- No Tier C / attorney contributor content or relationships

### Business / Operational

- No entity structure (LLC, etc.)
- No monetization implementation
- No legal disclaimer reviewed by attorney
- No contributor recruitment plan
- No content refresh / maintenance process defined

---

## Recommended Next Actions (In Suggested Order)

**1. Set up a reliable, reproducible query environment.**
The CJDT data needs to live in a proper database (PostgreSQL, DuckDB, or similar) where queries can be version-controlled, re-run, and verified. The Manus agent work was invaluable for exploration but isn't suitable for producing publication-quality numbers. This is infrastructure that unlocks everything else.

**2. Verify key DUI findings independently.**
Re-run the critical queries (jail classification, financial burden, non-conviction pathways, FCF comparison) in the new environment. Confirm or correct the numbers. This is the foundation for every page.

**3. Write the Battery profiling prompt and run it.**
Tests whether the pipeline transfers to a second charge type. Battery is the best candidate (high volume, interesting splits on AW and diversion, DV indicator as a natural situational dimension). The profiling results will either confirm the framework generalizes or reveal where it needs adjustment.

**4. Research diversion programs.**
Map which Florida counties have formal DUI diversion programs. This is high reader-benefit content that layers onto existing data. Can be done in parallel with technical work.

**5. Validate search demand.**
Run keyword research on the crisis-stage queries identified in the working notes. Confirms or adjusts which pages to prioritize and what URL structures to use.

**6. Build prototype of one page.**
The DUI hub charge page is the most complex and the most important. Build it with real (verified) data, full schema, interactive county element. Test schema against Rich Results Test. This is the proof of concept that determines technical approach for everything else.

**7. Extend to first situational page.**
Likely First DUI or DUI Refusal — whichever has strongest data support after verification.

---

## Key Principles To Maintain

These are the things most likely to get lost or overridden as new LLMs pick up tasks. Push back if a task prompt contradicts them.

1. **Reader benefit is the #1 priority.** Not data completeness, not SEO, not technical elegance. If it doesn't help the person charged with a crime, it doesn't go on the page. (V5 Section 2, Pillar 1)

2. **Interpretation, not display.** Never publish a raw CJDT number without understanding what it means. Cross-reference fields. Check for artifacts. Disclose limitations. This is the differentiator. (Working Notes Part 1)

3. **Honest methodology is the credibility.** Document everything. Disclose gaps. Tag confidence. If the data might be wrong, say so and say why. (V5 Section 24, Principles 3, 17, 18)

4. **Don't converge prematurely.** The DUI calibration informed the framework but didn't finalize it. Each new charge type will reveal things we didn't anticipate. Keep decisions open until data forces them closed. (Charge Framework Part 5)

5. **Don't apply old-paradigm SEO thinking.** Traffic volume is not the metric. Citation authority is. Low search volume doesn't mean low value. High page count doesn't mean high quality. (V5 Section 4, Section 25)

6. **All Phase 1A numbers are unverified.** Treat them as directionally correct exploration results, not publication-ready data. Every number that will appear on a published page needs independent verification in a controlled query environment.

---

## Things Other LLMs Consistently Get Wrong On This Project

Inherited from V5 Section 25, updated with Phase 1A experience:

1. **Defaulting to traffic-volume concerns.** "930-3,340 monthly searches" is not the addressable market. Every AI Overview answering a DUI question potentially cites our data.
2. **Treating FCF as failed rather than different.** FCF executes well. They're ahead on indexing and coverage. Our model is different, not superior by default. The advantage is in interpretation depth, not in their failure.
3. **Over-planning expansion before the first page is built.** Florida DUI first. Prove the thesis on one charge type in one state.
4. **Suggesting anti-extraction mechanisms.** We want LLMs to cite us. Don't build barriers to extraction.
5. **Recommending against statute/infrastructure pages.** Tier 1 pages are data anchors and internal linking infrastructure. They need to exist.
6. **Converging on page design before understanding the data.** Each charge type's editorial story is different. DUI is about sentencing interpretation. Battery might be about DV splits. Don't assume DUI's template transfers without profiling.
7. **Treating the data as ground truth.** CJDT is mandatory administrative reporting, not independently verified case outcomes. Clerk coding practices vary by county. The data represents what was officially reported. Always.
8. **Getting excited about a data finding and building the page around it.** The data serves the reader's questions. The page is organized by what the reader needs, not by what the data can show. (Lesson learned during Phase 1A when we almost built a "sentencing variance analysis" page nobody would search for.)
