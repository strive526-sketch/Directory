# Florida Build Document: Potential Approaches for Phase 1 Implementation

## Document Purpose

This document explores how the project could be built using Florida's CJDT dataset as the foundation. It is framed as potential approaches, not converged decisions. There are multiple viable paths for nearly every design choice described here. The purpose is to map those paths clearly enough that the person building it (or an LLM assisting the build) can make informed choices with full context of the tradeoffs.

This document assumes the reader has access to the v3 checkpoint and the v3 research findings amendment. It does not repeat strategic context already covered there.

---

## The Data We Have

### Source

Florida FDLE Criminal Justice Data Transparency (CJDT) Clerk Case dataset. Downloaded as a ZIP from Azure Blob Storage (direct URL, no login, no rate limits). 207 MB compressed, 1.84 GB uncompressed. Five CSV files totaling 4,092,482 charge-level records across 55 columns. [CONFIRMED via direct inspection.]

### What's Usable

**High-confidence fields (0% or near-0% missing, standardized values):**
- Disposition (Adjudicated Guilty, Adjudication Withheld, Pre-Trial Diversion, Dismissed, plus ~11 rare categories)
- STATUTE and FCIC_Category (charge identification)
- Level (Misdemeanor, Felony, Infraction) and Degree (First, Second, Third)
- Race, Ethnicity, Sex, Age
- Indigent (Yes, No, Not Available)
- COUNTY_DESCRIPTION and COUNTY_CODE
- JUDICIAL_CIRCUIT
- UNIQUE_CORRELATION_ID (links charges in the same case)
- PERSON_ID (links charges to the same defendant)
- DISPOSITION_DATE

**Moderately usable fields (10-36% missing, variable by county):**
- COUNSEL_CATEGORY (Private Attorney, Public Defender, Self or Unrepresented, etc.) -- 13% missing overall but 100% missing for Broward County. Usable only for counties that report it.
- SENTENCING_DATE -- 15-24% missing.
- COURT_COST -- 36% missing.
- SENTENCE_CONFINEMENT (County Jail, State Prison Facility) -- 66% missing but expected (only populated for confinement sentences).
- SENTENCE_PROBATION_DURATION_DAYS, MAXIMUM_TERM_DURATION_DAYS -- populated for sentenced cases.

**Not usable:**
- FINE, RESTITUTION -- 77-78% missing. Don't attempt financial penalty analysis.
- PROSECUTOR_FILING, SENTENCE_STATUS, various habitual offender flags -- 100% empty.
- US_CITIZENSHIP -- 78% "Not Available." Practically useless.
- STATUTE_SUBSECTION -- 92% missing (clerks embed subsections in the STATUTE field instead).

### DUI-Specific Subset

Approximately 340,000-350,000 DUI charge records identifiable by:
- FCIC_Category = "DUI-Unlawful Blood Alcohol" (cleanest filter)
- Or STATUTE LIKE '316.193%' with explicit exclusion of 316.1935 (Fleeing/Eluding) and 316.1939 (Refusal to submit to testing)

Both filters should be used together for cross-validation. FCIC_Category is recommended as the primary filter since it avoids the statute string-matching complexity.

### Design Decision: Charge-Level vs. Case-Level Analysis

The dataset is one row per charge, not one row per case. A single case (UNIQUE_CORRELATION_ID) can have charges with different dispositions -- one charge convicted, another dismissed.

This requires a design decision about how to define "case outcome." Potential approaches:

**Option A: Most-serious-outcome hierarchy.** Define a hierarchy (Adjudicated Guilty > Adjudication Withheld > Pre-Trial Diversion > Dismissed > other) and assign the case the most serious outcome of any charge in it. A case with one guilty charge and one dismissed charge is a "guilty" case. Strengths: simple, intuitive, commonly used in criminal justice research. Weaknesses: obscures plea bargaining dynamics where the serious charge is dismissed in exchange for a guilty plea on a lesser charge.

**Option B: Primary-charge-outcome.** Identify the most serious charge in each case (by Level/Degree) and use that charge's disposition as the case outcome. Strengths: captures what happened with the charge that mattered most. Weaknesses: "most serious" isn't always clear (two charges of the same level?), and the primary charge's outcome may not reflect the overall case resolution.

**Option C: Report at the charge level, not the case level.** Don't aggregate to case-level outcomes. Report "X% of DUI charges resulted in conviction" rather than "X% of DUI cases resulted in conviction." Strengths: avoids the entire aggregation problem, stays true to the data. Weaknesses: readers think in cases, not charges. "68% of DUI charges" is harder to interpret than "68% of DUI cases."

**Option D: Report both.** Publish charge-level statistics as the primary metric (transparent, unambiguous) and case-level statistics as a secondary metric with the hierarchy logic documented. Strengths: most complete picture. Weaknesses: more complex, potentially confusing to lay readers.

**Assessment:** Option C or D is likely best for Phase 1. Option C keeps things simple and avoids design decisions that might need to be revised. Option D provides the richest picture. The hierarchy logic for case-level aggregation should be developed during Phase 1 manual processing and documented in the methodology. This is one of the decisions that goes into the editorial decision register.

---

## What Could Be Built: Tier 1 (Statute Pages)

### Candidate First Charge Type: DUI (Florida Statute 316.193)

**Why DUI first:**
- Highest commercial value (DUI attorney market is massive -- 27K-37K monthly Florida DUI searches)
- Clean filterable subset (~340K records)
- Well-understood charge category (less normalization ambiguity than e.g. drug offenses with multiple schedules)
- High-intent searchers (someone just got arrested)
- Strong Tier 2 charge page potential ("DUI Florida" is a high-volume query)

**What a DUI statute page for a specific county could contain:**

Section 1 -- BLUF: "Florida Statute 316.193 is the state's DUI law. In [County], based on [N] cases from [date range], approximately X% of DUI charges result in conviction, Y% receive adjudication withheld, and Z% are dismissed." (40-50 words, directly answerable by AI Overview, schema-marked as StatisticalVariable.)

Section 2 -- What this charge means: Plain-English explanation of 316.193. What constitutes DUI in Florida. BAC thresholds. Implied consent. (Tier A content, but written in the project's information sequencing, not in the standard legal content format of leading with max penalties.)

Section 3 -- What typically happens in [County]: The disposition distribution with actual percentages. Adjudication Withheld explained (what it means, what it preserves, how it differs from full conviction). Pre-Trial Diversion rates. Dismissal rates. This is the core Tier B content. Presented as a clear data visualization (bar chart or table) with methodology note.

Section 4 -- How outcomes vary: If the county's rates diverge meaningfully from the statewide average, note it. "The dismissal rate in [County] is X%, compared to the statewide average of Y%." If they don't diverge meaningfully, don't force a finding -- just present the county data in context.

Section 5 -- Related charges: What other charges are commonly filed alongside DUI in this county? (Built from UNIQUE_CORRELATION_ID grouping.) "In X% of cases involving a 316.193 charge, defendants also faced charges for [charge], [charge], and [charge]." This is a cross-reference no other legal site publishes.

Section 6 -- Charge severity breakdown: What percentage are misdemeanor DUI vs. felony DUI in this county? How do outcomes differ by severity level?

Section 7 -- Sentence data (for convicted cases): Confinement type distribution (County Jail vs. State Prison), probation duration distribution, maximum term distribution. Presented as ranges, not averages, to reflect the actual spread.

Section 8 -- What to do next: Procedural guidance. Next court dates. How to find an attorney. This is where the contributor placement naturally lives.

Section 9 -- Demographic context (potential -- see considerations below): Outcome distribution by race, sex, age cohort. Presented neutrally with explicit methodology.

Section 10 -- Full legal text: The actual statute text. With LegalCode schema.

Section 11 -- Methodology: Data source, date range, sample size, exclusion criteria, normalization decisions, known limitations (no BAC data, incomplete county coverage, COUNSEL_CATEGORY gaps if applicable).

### Schema Implementation for a Statute Page

```
LegalCode -- on the statute text section
Dataset -- on the page overall, referencing the synthesized court outcome data
StatisticalVariable -- on each key metric (conviction rate, dismissal rate, etc.)
FAQPage -- wrapping the key sections as Q&A pairs ("What happens with a DUI in [County]?" → Section 3)
Article -- on the editorial content, with author attribution
Person + hasCredential -- on the contributor section (if present)
BreadcrumbList -- navigation context
dateModified -- page freshness signal
```

### Considerations for Demographic Cross-References

The CJDT data includes race, ethnicity, sex, and age for every record. Cross-referencing outcomes by demographics is technically trivial and produces the highest-newsworthy findings (see v3 review notes, Flag 6). But there are considerations:

**The case for including it from the start:** The data is there. Not publishing it is a choice to suppress available information. The content neutrality principle says report what the data shows without editorial interpretation. Demographic breakdowns are standard in criminal justice research (MFJ includes them). Excluding them creates a gap that invites criticism ("why aren't you showing the racial breakdown?").

**The case for phasing it in:** Demographic disparity findings generate orders of magnitude more attention (and political heat) than simple disposition rates. Publishing them on a new platform with no established credibility could invite backlash before the site has built trust. The content neutrality framing may not be enough to prevent the platform being perceived as advocacy if the first thing people see is racial disparity data. Starting with disposition and sentencing data, establishing credibility, and then adding demographic breakdowns in Phase 2-3 might be a more sustainable sequence.

**The case for making it available but not leading with it:** Include demographic data on the page but don't make it the BLUF or the headline metric. Lead with overall disposition rates. Provide demographic breakdowns as a secondary analysis section deeper on the page. This satisfies transparency without making demographic disparities the platform's defining first impression.

No recommendation. This is a framing and sequencing choice with real tradeoffs.

---

## What Could Be Built: Tier 2 (Charge Pages)

### Example: "DUI in Florida" Page

This page would aggregate data from all Florida counties' DUI statute pages. It's the primary discovery surface for the highest-volume queries ("DUI Florida," "Florida DUI penalties," "first offense DUI Florida").

**Potential structure:**

Section 1 -- BLUF: "In Florida, DUI is prosecuted under Statute 316.193. Based on [total N] cases across [X] Florida counties from [date range], approximately X% of DUI charges statewide result in conviction, Y% receive adjudication withheld, and Z% are dismissed. Outcomes vary significantly by county."

Section 2 -- What DUI means in Florida: Plain-English explanation. BAC thresholds. Implied consent law. Enhanced penalties for repeat offenses. This section draws from Tier A data but is written in the project's information sequencing.

Section 3 -- What typically happens statewide: Statewide disposition distribution. Statewide sentence distribution for convicted cases. Statewide charge severity breakdown (misdemeanor vs. felony DUI).

Section 4 -- How outcomes vary by county: This is the synthesis content that makes this page genuinely novel. A table or visualization showing disposition rates across counties. Counties with notably high or low dismissal/conviction rates highlighted. The variance itself is the finding. If Broward's dismissal rate is 48% and the statewide average is 5%, that's a data point worth seeing.

Section 5 -- County-by-county data: Links to each county's individual DUI statute page (Tier 1) where the detailed data lives. This is the internal linking structure that distributes authority from the high-traffic Tier 2 page to the granular Tier 1 pages.

Section 6 -- Penalties: First offense, second offense, third offense, felony DUI. Presented as a structured table with FAQPage schema wrapping each tier. This is the content that competes with FindLaw and Shouse for penalty-related queries.

Section 7 -- Related charges: Statewide charge co-occurrence patterns for DUI. What other charges commonly accompany a DUI filing?

Section 8 -- Timeline: How long does a DUI case take to resolve in Florida? Statewide distribution with county-level variance if meaningful.

Section 9 -- What to do next: Procedural guidance. Links to finding an attorney. Contributor placement (if applicable at the charge-page level -- this is a design choice).

Section 10 -- Methodology: Comprehensive documentation for the statewide synthesis.

### How Charge Pages Pull Data Upward

The key architectural principle: the charge page doesn't duplicate data from statute pages. It aggregates and presents it at a higher level, with links down to the granular data. A reader who wants the statewide picture reads the charge page. A reader who wants their specific county's numbers follows the link to the statute page. The data exists once (in the database) and is rendered at multiple levels.

---

## What Could Be Built: Tier 3 (Synthesis Pages)

### These Only Exist When the Data Earns Them

Tier 3 pages are not produced programmatically. They're produced when the data analysis reveals a finding worth publishing. The editorial gate applies: intent must exist, the data must say something, and the comparison must be structurally valid.

### Potential First Synthesis Findings (to be validated against actual data)

These are hypotheses about what the Florida data might reveal. They become Tier 3 pages only if the data confirms them:

**County-level variance in DUI outcomes.** If dismissal rates vary from 5% to 48% across Florida counties for the same charge, that's a finding. The variance itself is the story. "We analyzed [N] DUI cases across [X] Florida counties. Here's how outcomes differ depending on where you're arrested."

**Outcomes by representation type.** For counties that report COUNSEL_CATEGORY: how do outcomes differ for defendants with private attorneys vs. public defenders vs. self-represented? This is buildable for a subset of counties and is one of the highest-value cross-references.

**Rural vs. metro cohort analysis.** Aggregate small-population Florida counties into a rural cohort. Aggregate large-population counties into a metro cohort. Compare DUI outcome distributions between cohorts. This tests whether court size/resources correlate with outcomes.

**Temporal trends.** How have DUI disposition patterns in Florida changed from 2018 to 2025? Has the conviction rate increased or decreased? Have specific counties shifted? This requires only the DISPOSITION_DATE field (which is 100% populated) and the disposition field.

**Charge co-occurrence patterns.** When someone faces a DUI charge, what other charges are filed in the same case? How often does a DUI come with an open container violation, a driving-on-suspended charge, or a resisting arrest charge? Do multi-charge cases have different outcomes than single-charge DUI cases?

**First-offense vs. repeat-offense patterns.** Using PERSON_ID to identify defendants who appear multiple times in the dataset. How do outcomes differ for first-time vs. repeat DUI defendants? (Note: this analysis is limited to the 2018-2026 dataset window. A defendant with no prior records in this dataset may have prior history before 2018.)

### The 50-State Transparency Audit as a First Publication

A potential Tier 3/4 asset that doesn't require any court data synthesis: "We audited all 50 states' criminal court data transparency. Here's what we found." This uses the 50-state scan research already completed. Published as a polished article with a state-by-state visualization, methodology documentation, and the key structural findings (the commercial intermediary problem, the statutory mandate correlation, the DUI data gap, the Virginia anomaly).

This could be the platform's first published piece -- generating authority, media interest, and citation signals before any court data is synthesized. Reform advocates, journalists, and researchers would all have reasons to reference it. The transparency gap itself is a newsworthy finding.

Considerations: This piece positions the platform as a criminal justice data transparency resource from day one. It establishes the editorial voice (neutral, data-driven, methodology-transparent) before any politically sensitive county-level data is published. It creates backlinks and domain authority that benefit every subsequent page.

This could also serve as a test of the Tier 4 distribution strategy -- seeing which communities engage with it, which distribution channels work, what formats generate the most traction.

---

## What Could Be Built: Tier 4 (Distribution Assets)

### For Each Synthesis Finding, Multiple Formats

Once a Tier 3 finding is confirmed (data earns it, editorial gate passed), it can be rendered in multiple distribution formats:

- The synthesis page itself (long-form reference content on the platform)
- A data visualization (chart, map, or infographic suitable for social sharing)
- An executive summary (2-3 paragraph version for newsletter distribution or media pitching)
- A downloadable methodology document (establishes credibility, enables independent verification)
- Raw aggregated data tables (downloadable CSV for researchers who want to verify or extend the analysis)

The same finding, multiple formats, multiple distribution channels. One synthesis effort produces five distribution-ready assets.

### Potential Distribution Channels for Florida Criminal Justice Data

Criminal defense attorney communities on LinkedIn and legal forums (they'll reference county-level outcome data in consultations and marketing).

Criminal justice reform organizations (county-level variance data is exactly what reform advocates need for policy arguments).

Florida-specific journalism outlets (local and regional reporters covering courts, criminal justice, policy).

Law school faculty and clinics (academic research community that cites county-level criminal justice statistics).

Legal tech communities (professionals building tools who want to know about available data sources).

Policy research organizations (Brennan Center, Marshall Project, ProPublica -- organizations that cover criminal justice data).

---

## Technical Implementation Considerations

### Site Architecture Options

**Option A: Static site generator (e.g., Hugo, Eleventy, Astro) with pre-rendered pages.** Generate all pages at build time from the database. Pure static HTML -- maximally crawlable, fastest load times, simplest hosting. Schema markup baked directly into templates. Rebuild triggered by data refreshes. Strengths: performance, crawlability, simplicity. Weaknesses: rebuild time grows with page count, dynamic features require workarounds.

**Option B: Server-rendered application (e.g., Next.js, SvelteKit) with database backend.** Pages rendered on request from a structured database. Allows dynamic query of data. Schema markup generated from database fields. Strengths: flexible, handles large page counts without rebuild time, supports future features like attorney dashboards. Weaknesses: more complex infrastructure, server costs, potential crawl budget issues.

**Option C: Hybrid -- static pages for content, dynamic components for data visualization.** Core page content is static HTML with schema markup. Data visualizations (charts, maps) load client-side from a lightweight API. Strengths: combines crawlability of static with interactivity of dynamic. Weaknesses: requires two systems.

**Assessment:** Option A is likely simplest for Phase 1 if the page count stays manageable (20-50 pages for seed content). Option B becomes necessary at scale or if interactive features are needed. The choice depends on the operator's technical preferences and the expected pace of scaling.

### Database Design

Regardless of site architecture, the underlying data should be stored in a structured, queryable database (not just CSV files). This enables:

- Multiple page types (statute pages, charge pages, synthesis pages) querying the same data
- Refresh cycles updating the database without regenerating every page
- Future API access for Phase 2+ monetization
- Ad-hoc analysis for identifying synthesis findings

Schema suggestion: PostgreSQL or SQLite for Phase 1. The CJDT data maps cleanly to a relational model. Key tables: charges (one row per charge record), cases (grouped by UNIQUE_CORRELATION_ID), counties, statutes. Derived tables: disposition_distributions (pre-computed per county per statute), co_occurrence_patterns, sentence_distributions.

### Hosting and Domain

Not a critical decision for Phase 1. Any modern hosting that serves static HTML fast and supports custom domains. The domain name should signal data/reference authority, not law firm marketing. Something that sounds institutional rather than commercial. But this is the partner's domain (literally and figuratively) as the SEO specialist.

---

## Phase 1 Execution Sequence (Potential)

This is one possible execution sequence. Other orderings may be equally valid.

**Step 1: Data ingestion.** Download CJDT Clerk Case ZIP. Load into database. Verify record counts, column names, and data types against the research report's data dictionary. Flag any discrepancies.

**Step 2: DUI subset extraction.** Filter for DUI records using FCIC_Category and cross-validate with STATUTE field. Verify record count (~340K expected). Examine the subset: which counties have enough DUI records for meaningful analysis? What's the distribution of records by county, by year?

**Step 3: First synthesis -- statewide DUI disposition distribution.** Calculate overall Florida DUI disposition rates (conviction, adjudication withheld, pre-trial diversion, dismissed). This is the first net-new statistic. Check if it exists anywhere else. If not, it's net-new by definition.

**Step 4: County-level breakdown.** Calculate the same disposition distribution per county. Identify counties with meaningful variance from the statewide average. This is where the editorial gate calibration begins. What threshold of variance constitutes "meaningful"? Log the judgment calls.

**Step 5: Cross-references.** For counties that report COUNSEL_CATEGORY: calculate outcomes by representation type. Calculate outcomes by charge severity. Calculate co-occurrence patterns. Calculate temporal trends. Each cross-reference that produces a genuinely novel finding goes into the editorial decision register.

**Step 6: Page mockups.** Build 2-3 prototype pages from real data: one county-level statute page, one statewide charge page, and (if the data supports it) one synthesis page showing cross-county variance. Apply the full schema stack. Test against schema validation tools. Test how the page renders in Google's Rich Results Test.

**Step 7: Review and iterate.** Review the prototypes. Does the information sequencing work with real data? Does the schema implementation pass validation? Does the page look like something an attorney would want to be associated with? Does it look like something a journalist would cite? Iterate.

**Step 8: Seed content production.** If the prototypes pass review, produce the initial set of pages. The exact count depends on how many counties have sufficient DUI data for meaningful analysis. Could be 20 pages, could be 50. Quality over quantity -- every page must pass the Tier B minimum gate.

**Step 9: Publication and observation.** Publish. Submit to Google Search Console. Monitor for indexation, ranking signals, AI Overview citation, organic backlinks. Begin the 60-90 day authority verification period.

**Parallel track: The 50-state transparency audit.** While court data pages are being built, the 50-state transparency audit can be polished and published as the platform's first Tier 4 distribution asset. This builds domain authority and establishes the platform's editorial voice before the county-level data pages start ranking.

---

## Open Design Decisions

The following decisions need to be made during Phase 1. They're listed here so they're not forgotten:

1. **Charge-level vs. case-level reporting** -- how to handle multi-charge cases (Options A-D above).
2. **Demographic data inclusion and sequencing** -- include from launch, phase in, or make available but not lead with.
3. **Minimum sample size threshold** -- below what N do we not publish county-level statistics? Needs calibration from actual data variance.
4. **Minimum variance threshold for synthesis pages** -- what constitutes "meaningful" divergence from average? Needs calibration from Phase 1 judgment calls logged in the editorial decision register.
5. **Counties to exclude** -- which counties have data quality too poor to publish? (Broward for attorney type analysis, counties with very low record counts overall.)
6. **Adjudication Withheld handling** -- how to present this Florida-specific disposition to users unfamiliar with it. This is both an educational content challenge and a normalization challenge for future cross-state comparison.
7. **Site architecture choice** -- static, server-rendered, or hybrid.
8. **Domain name and branding** -- signals institutional authority, not commercial legal marketing.
9. **Schema implementation priority** -- FAQPage and LegalCode first per research findings, with Dataset/StatisticalVariable added alongside.
10. **Contributor page template** -- what does the contribution section look like? What are the templated options for varying willingness to share? This doesn't need to be decided until Phase 5 but the page design should leave space for it.

---

## What Success Looks Like After Phase 1

At the end of Phase 1 (estimated 4 weeks), the project should have:

1. A working database of Florida CJDT data, queryable and normalized.
2. Net-new DUI statistics for Florida that don't exist elsewhere on the public internet.
3. A clear picture of which cross-references are meaningful and which fall in the dead man's zone.
4. 2-3 prototype pages with real data, full schema markup, and proper methodology documentation.
5. A structural compatibility map documenting what's buildable and what's not from this dataset.
6. An editorial decision register logging every publish/kill judgment call.
7. A cost and timeline profile for producing pages at scale.
8. A "walk away number" for pre-revenue investment.
9. Concurrent results from traffic decomposition and MFJ audit to validate the demand thesis.

If all of these check out, Phase 2 (seed content production of 20-50 pages) proceeds with confidence. If any of them fail, the project has identified the failure point before significant resources were committed.
