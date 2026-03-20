# DUI Florida: Page Architecture & Content Map

**Purpose:** Define every page that should exist for DUI in Florida, what goes on each page, and why — based on actual validated data availability and reader benefit. This is the bridge between the V5 framework and the build.

**Governing principle:** Every element on every page answers a question a real person in this situation is actually asking. If it doesn't serve the reader, it doesn't appear in the visible content (it may exist in schema for machine readability).

---

## Page Inventory Summary

| Page | Type | Reader | Data Confidence |
|---|---|---|---|
| Florida Statute 316.193 | Statute (Tier 1) | Person reading paperwork, attorneys, LLMs | High |
| DUI in Florida | Charge Hub (Tier 2) | Person searching "DUI Florida" | High |
| First DUI in Florida | Situational (Tier 2) | First-time offender, highest intent | Moderate (MDM_PERSON_ID lower bound) |
| Second / Repeat DUI in Florida | Situational (Tier 2) | Repeat offender | Moderate (same MDM caveat) |
| Felony DUI in Florida | Situational (Tier 2) | 3rd+ offense or serious injury | High (Level field is clean) |
| DUI Refusal in Florida | Situational (Tier 2) | Person who refused breathalyzer | High (316.1939, 11K+ records) |
| DUI with Injury in Florida | Situational (Tier 2) | Person whose DUI involved injury | Moderate (statute subsection filtering needed) |
| DUI in [County] | County (Tier 2, conditional) | Person searching their specific county | High for qualified counties |
| Florida Statute 316.1939 | Statute (Tier 1) | Person reading refusal citation | High |

Potential additional pages (evaluate after initial build):
- DUI and Driving on Suspended License (co-occurring charge pattern)
- DUI Diversion Programs in Florida (synthesis of county-level diversion data)
- How Much Does a DUI Cost in Florida (financial burden synthesis)
- Related statute pages for top co-occurring charges (322.34, 843.02)
- Fleeing/Eluding (316.1935) — 13,900 records 2023-2025, viable standalone charge type for expansion pipeline

---

## Page 1: Florida Statute 316.193

### Who lands here
Person just charged, reading the statute number from their citation or arrest paperwork. Attorneys. Paralegals. LLMs seeking primary statute text.

### What they're asking
- "What does 316.193 mean?"
- "What am I charged with?"
- "What are the penalties for this?"

### Content sections (in order)

**1. Plain English summary (BLUF)**
What this statute is. One paragraph. "Florida Statute 316.193 is Florida's DUI law. It covers driving or being in actual physical control of a vehicle while under the influence of alcohol, drugs, or controlled substances, or with a blood/breath alcohol level of .08 or higher."

No data needed. Just clarity.

**2. Penalty structure by offense tier**
Statutory penalties laid out clearly. First offense, second within 5 years, second outside 5 years, third within 10 years (felony), fourth+ (always felony). Include Trenton's Law changes (effective October 2025).

Source: Statute text. Standard legal reference content. Our version is cleaner and better organized than most but this is table-stakes content.

**3. Statewide disposition snapshot**
Brief data anchor: "Based on [N] DUI cases statewide (2023-2025), 93.4% result in conviction. However, sentencing outcomes vary significantly by county." Links to charge page for full picture.

Data: Clerk dataset, DUI filter, 2023-2025. High confidence.

**4. Related statutes**
- 316.1939 — Refusal to submit to testing (link to its own statute page)
- 316.1935 — DUI causing serious bodily injury or death
- 322.34 — Driving on suspended license (common co-charge)
- 322.2616 — Administrative license suspension (10-day rule)
- 948.01 — Adjudication Withheld explanation (if AW applies here)

**5. Full statute text**
Complete text of 316.193 with subsections. Bottom of page. LegalCode schema. Most readers won't read this but it's the primary source anchor.

### Schema
LegalCode (unique — no competitor has this), Dataset (statewide disposition snapshot), BreadcrumbList, FAQPage (2-3 core questions).

---

## Page 2: DUI in Florida (Charge Hub)

### Who lands here
The main audience. Person searching "DUI Florida," "DUI charges Florida," "Florida DUI penalties." Pre-charge worried, recently charged, comparison-shopping attorneys, family researching. Mixed cognitive states — some in acute crisis, some in deliberate research mode.

### What they're asking (in order of urgency)
1. "What am I actually facing?" (realistic outcomes, not worst case)
2. "Am I going to jail?" (the #1 fear)
3. "How much is this going to cost me?"
4. "Is there any way to avoid a conviction?"
5. "What's different about MY county?"
6. "What else am I charged with?"
7. "Should I get a lawyer?"
8. "What do I do right now?"

### Content sections (in order, mapped to questions)

**1. BLUF — What you're realistically facing (answers Q1)**

40-50 words. "If you've been charged with DUI in Florida, you're facing a serious situation — 93.4% of DUI charges result in conviction statewide. But what that conviction actually looks like — whether you serve jail time, how much it costs, and whether alternatives exist — depends heavily on your county and circumstances."

Data: Statewide conviction rate. High confidence.

Why this works: It's honest without being terrifying. It acknowledges the severity (93%) while immediately signaling that there's more to the story (county variance, circumstances). The reader keeps reading instead of panicking and bouncing.

**2. "Am I going to jail?" — The sentencing reality (answers Q2)**

This is the section that differentiates us from everyone. Not the statutory maximum. Not the raw jail percentage. The interpreted reality.

Content:
- Statewide overview: "[X]% of DUI convictions include a jail component. But what 'jail' means varies enormously by county."
- Explanation of the three patterns: some counties record booking credit as jail time (you're not going back), some impose real sentences (median 30-90 days), some are mixed
- Statewide median sentence for cases with real jail time: [X] days
- Probation: "The overwhelming majority of DUI convictions include 12 months of probation regardless of county."

Data: Jail classification metadata (42 counties classified). Sentence length distribution. CTS analysis. All validated.

This is where the interactive county element lives (see below).

**3. "How much will this cost?" — Total financial burden (answers Q3)**

Content:
- Statewide median court-imposed total (fines + court costs): $1,468
- Range across counties: $931 (Hillsborough) to $2,912 (Escambia)
- Framing: "This is court-imposed costs only. Additional costs typically include: DUI school (~$350), license reinstatement (~$275), vehicle impound fees, ignition interlock device (if ordered), and substantially increased insurance premiums (FR-44 requirement). Total first-year cost of a DUI conviction in Florida commonly ranges from $X,000 to $X,000."

Data: Financial burden query. 80.1% coverage statewide. County-specific medians for top 20+. Gaps disclosed (Lee, Broward at 0%).

Non-data elements: The DUI school cost, reinstatement fee, and FR-44 requirement are publicly documented fixed costs. We cite source for each. The insurance premium increase is variable but well-documented range estimates exist.

**4. "Is there any way out?" — Non-conviction pathways (answers Q4)**

Content:
- Statewide non-conviction rate: ~6.6% (dismissal + diversion + acquittal combined)
- BUT massive county variance: Orange County 40.9% non-conviction (28.7% diversion), Collier 0.7%
- What diversion means: reduction to reckless driving, avoid DUI conviction on record, specific program requirements
- Named programs where known: Hillsborough RIDR, Pinellas DROP (research needed for full county list)
- Honest framing: "Eligibility for diversion depends on your specific circumstances including BAC level, prior record, and county policies. These statistics reflect aggregate outcomes, not individual odds."

Data: Non-conviction pathway analysis. High confidence statewide and for major counties.

This is one of the most valuable sections. Nobody aggregates this. Attorney sites say "we may be able to get your charges reduced" without data. We say "in your county, [X]% of DUI cases were resolved through diversion programs."

**5. Your county matters — Interactive element (answers Q5)**

County selector. Reader picks their county. See their county's profile compared to statewide:

For each county (where data supports):
- Conviction rate
- Jail rate WITH interpretation (booking artifact / real jail / mixed — using the correct presentation template from classification)
- Median sentence for real jail cases
- Median total financial burden (fines + costs)
- Non-conviction pathway rate (diversion + dismissal + acquittal)
- Sample size and date range

For low-data counties: reduced display with appropriate caveats.
For Miami-Dade: explicit data completeness warning.

Data: All validated, classified, and threshold-tested. 42 counties with full classification, 23 with limited display, 6 suppressed.

Schema: Full county-level Dataset in JSON-LD (machine sees everything, human sees their county). This is the proto-API.

**6. "What else am I charged with?" — Co-occurring charges (answers Q6)**

Content:
- "DUI charges frequently accompany other charges from the same incident."
- Top co-occurring charges with plain-English explanation:
  - 316.1939 — Refusal to submit to testing (link to refusal page)
  - 322.34 — Driving with suspended license
  - 843.02 — Resisting officer (without violence)
  - County ordinance violations
- "In [statewide], the average DUI case involves [1.48] charges."

Data: Co-occurrence from UNIQUE_CORRELATION_ID grouping. High confidence.

Why it matters: Many people don't realize they're facing multiple charges. This prepares them for what their attorney will discuss.

**7. "Should I get a lawyer?" — Attorney representation context (answers Q7)**

Content (only for counties with good COUNSEL_CATEGORY data):
- Outcome distributions by representation type — with heavy confounding disclosure
- Framing: "These statistics do not control for case severity, prior record, or pre-trial detention status. Defendants with private attorneys may have different case characteristics than those with public defenders."
- Genuinely useful context: the data exists, it says something, but what it says requires careful interpretation

For counties without data (Broward, Miami-Dade): "Attorney type data is not available for this county."

Data: COUNSEL_CATEGORY, ~60% of counties. Moderate confidence due to confounders.

**8. "What do I do right now?" — Next steps**

Content:
- Immediate timeline: 10-day rule for license hearing with DHSMV
- Arraignment: what it is, what to expect
- Whether to request a formal review hearing
- Contributor placement (Phase 2+): this is where the attorney contextually belongs

No data needed. Procedural guidance sourced from statute and DHSMV rules.

**9. Penalty structure reference**

Statutory penalties by offense tier. Similar to statute page but in the charge context. For completeness — the reader who scrolls this far wants the full reference.

**10. Methodology**

Brief inline: source, date range, sample size, key caveats per section.
Linked full methodology: detailed normalization rules, field definitions, known limitations, county-specific data quality notes.

### Schema stack
Dataset (statewide + per-county in JSON-LD), FAQPage (top 5-7 questions derived from content), Article, ClaimReview (on BLUF statistic and key findings), BreadcrumbList, Organization as creator.

---

## Page 3: First DUI in Florida

### Who lands here
Person charged with DUI for the first time. Highest intent. Most scared. Searching "first DUI Florida," "first time DUI penalties Florida," "what happens first DUI Florida."

### What they're asking
- "What happens for a first offense specifically?"
- "Is this going to ruin my life?"
- "Can I avoid a conviction?"
- "What's the minimum I'm looking at?"

### How it differs from hub
Everything filtered to first-offense reality. The hub shows all DUI data. This page shows ONLY what's relevant to someone facing their first charge. Data excludes repeat offenders where identifiable (MDM_PERSON_ID filter, lower bound methodology disclosed).

### Content sections

**1. BLUF**
"A first DUI in Florida is a misdemeanor. While conviction rates are high, sentencing for first offenses is typically the lightest tier — and some counties offer diversion programs that can result in reduced charges."

**2. First-offense penalties (statutory)**
Statutory minimums and maximums for first offense specifically. Not the full penalty table — just first offense. Readers don't need to see felony DUI penalties here (V5 negative space principle).

**3. What actually happens — first-offense sentencing reality**
Same sentencing data structure as hub, but filtered to first-offense cases where MDM_PERSON_ID allows identification. If the filter produces stable results: show first-offense-specific conviction rate, jail rate (with interpretation), financial burden.

If MDM filter is too lossy or unstable: show overall data with caveat "These statistics include all DUI cases. First-offense cases may differ — data limitations prevent precise first-offense filtering. See methodology."

**4. Diversion — your strongest pathway**
Expanded section on diversion. This is MORE relevant here than on the hub because first offenders are the primary diversion candidates.
- County-specific diversion rates
- Named programs (RIDR, DROP, others)
- What diversion typically involves (DUI school, evaluation, community service, probation, charge reduction to reckless)
- What it means for your record (no DUI conviction)

**5. County interactive (first-offense filtered where possible)**

**6. The 10-day license rule**
More prominent here than on hub. First-time offenders are most likely to not know about the DHSMV administrative hearing deadline.

**7. What to do right now — first offense specific**

### Methodology caveat
"First offense is defined as no prior DUI charge identified for the same individual in the FDLE CJDT dataset (2018-present) using FDLE's master data matching algorithm. Individuals with prior DUIs before 2018 or in jurisdictions not captured by this dataset may not be identified. This represents a conservative estimate — actual first-offense rates may be higher."

---

## Page 4: Second / Repeat DUI in Florida

### Who lands here
Person facing second or subsequent DUI. Different emotional state — more fear (knows the system escalates), possibly more cynicism. Searching "second DUI Florida," "2nd DUI penalties," "DUI second offense within 5 years."

### How it differs
- Penalty table focused on second offense tiers (within 5 years vs outside 5 years)
- Mandatory minimums are harsher and must be prominent (10-day mandatory jail for second within 5 years)
- Diversion is largely off the table — set honest expectations
- The "within 5 years" distinction is critical and date-specific
- MDM_PERSON_ID filtered to individuals with prior DUI charges

### Content sections
1. BLUF — acknowledges the escalation honestly
2. Penalty structure — second offense tiers (within 5 years is the critical split)
3. Sentencing reality — filtered to repeat offenders where identifiable
4. Financial burden — likely higher, show if data supports
5. County interactive — repeat offender outcomes where data supports
6. Limited alternative pathways — honest about reduced options
7. What's different this time — mandatory minimums, IID requirement, longer license revocation
8. Trenton's Law impact — October 2025 changes to repeat offender penalties

---

## Page 5: Felony DUI in Florida

### Who lands here
Person facing third DUI within 10 years, fourth lifetime, or DUI with serious injury/death. Searching "felony DUI Florida," "3rd DUI Florida," "DUI manslaughter Florida."

### How it differs
Radically different outcome profile. State prison enters the picture. This is the most serious DUI page.

### Content sections
1. BLUF — "A felony DUI in Florida carries the possibility of state prison. This page covers what the data shows about felony DUI outcomes."
2. What makes a DUI a felony — the specific triggers (3rd in 10 years, 4th lifetime, serious injury, death)
3. Sentencing reality — filtered to Level = 'Felony'. State prison rate, sentence length distribution. Data is clean on the Level field.
4. Financial burden at felony level
5. County interactive — felony-only outcomes
6. The long-term consequences — felony record, voting rights, firearms, employment (non-data, sourced from statute)
7. Related charges — 316.1935 (DUI with serious bodily injury), DUI manslaughter

Data: Level/Degree field is clean. Felony DUI subset from our profiling. Smaller N but sufficient statewide.

---

## Page 6: DUI Refusal in Florida

### Who lands here
Person who refused breathalyzer/chemical test. Panicking specifically about the refusal. Searching "refused breathalyzer Florida," "DUI refusal penalties," "what happens if you refuse breathalyzer Florida."

### What they're asking
- "Did refusing make things worse?"
- "Can I still be convicted without a breath test?"
- "What's the penalty for refusing?"
- "Was I supposed to refuse?" (retrospective anxiety)

### Content sections
1. BLUF — "Refusing a breathalyzer in Florida triggers automatic consequences, but the refusal charge itself is often resolved as part of the overall DUI case."
2. What refusing triggers — immediate administrative license suspension (separate from court case), refusal goes on DHSMV record
3. The dual-track reality — criminal case (DUI) and administrative case (license) are separate. Explain both.
4. How refusal charges are typically resolved — data shows 63% co-occur with standard DUI, refusal is often part of plea negotiations
5. Disposition comparison — refusal vs standard DUI outcomes side by side. Show the data.
6. Trenton's Law changes — October 2025 changed refusal penalties specifically
7. The 10-day DHSMV hearing — even MORE critical for refusal cases
8. County interactive — refusal outcomes by county where volume supports

Data: 316.1939 analysis. 11,464 records. High confidence. Co-occurrence data validated.

### This page also serves as Statute Page for 316.1939
Include LegalCode schema for the refusal statute. Dual-purpose page.

---

## Page 7: DUI with Injury in Florida

### Who lands here
Person whose DUI involved an accident with injuries. Most serious situational page before felony. Searching "DUI with injury Florida," "DUI accident injury penalties."

### Data reality
DUI causing serious bodily injury is 316.193(3)(c) — a SUBSECTION of the main DUI statute, not a separate statute number. (316.1935 is actually Fleeing/Eluding, a different charge entirely.) Whether we can isolate injury cases depends on STATUTE_SUBSECTION field, which is only 43% populated overall. Feasibility check pending — the field may be better populated for serious felony charges.

If subsection filtering works: build page with injury-specific outcome data.
If not: build page with statutory/procedural content plus general felony DUI data (Level = 'Felony' filter, which IS clean). Disclose: "Florida's public court data does not separately identify DUI cases involving injury at the disposition level. Felony DUI outcomes shown here include all felony-level DUI cases."

Either way, the page is worth building — high-intent search query, serious situation, reader needs information regardless of data granularity.

### Content sections
1. BLUF — what DUI with injury means under Florida law
2. What makes this a felony — the severity triggers in 316.193(3)
3. Penalty structure — felony penalties, state prison possibility, restitution
4. Outcome data — injury-specific if filterable, felony DUI if not (with disclosure)
5. How this differs from standard DUI — the severity escalation, civil liability, restitution
6. County interactive (felony DUI filtered)
7. Long-term consequences — felony record implications

### Additional finding: Miami-Dade data gap diagnosis
316.1935 (Fleeing/Eluding) shows 1,246 Miami-Dade records vs only 167 standard DUI. Confirms Miami-Dade submits felony-level cases normally — the data gap is specific to misdemeanor DUI. Updated disclosure: "Miami-Dade County appears to fully report felony-level cases but substantially underreports misdemeanor DUI dispositions to FDLE."

---

## County Pages (Conditional)

### Criteria for standalone county page
From V5, updated with data reality:
1. Sufficient volume (>500 DUI convictions 2023-2025)
2. Demonstrated search demand (people search "DUI [county name]")
3. Meaningfully differentiated outcomes AND/OR notable characteristics (formal diversion program, data anomaly requiring explanation, extreme sentencing pattern)

### Strong candidates based on data
- **Orange County** — 40.9% non-conviction rate, 28.7% diversion. Completely different DUI landscape. Booking artifact jail pattern. Page practically writes itself.
- **Duval County** — Booking artifact poster child. 86% "jail" that isn't jail. Readers need this explained.
- **Pinellas County** — DROP program, real jail pattern, high volume.
- **Hillsborough County** — RIDR program, real jail, highest DUI volume.
- **Escambia County** — Highest financial burden ($2,912 median), 6.4% non-conviction (highest among high-volume real-jail counties).
- **Pasco County** — Harshest real-jail pattern (90 day median, 10% CTS coverage).

### County page template
1. BLUF — "Here's what DUI looks like specifically in [County]."
2. Sentencing reality — with correct interpretation template (artifact/real/mixed)
3. Financial burden — county-specific
4. Non-conviction pathways — county-specific, name diversion programs if applicable
5. How [County] compares — brief statewide context
6. Co-occurring charges in this county (if pattern differs from statewide)
7. Attorney representation data (if COUNSEL_CATEGORY coverage >80%)
8. Methodology with county-specific data quality notes

---

## Related Statute Pages (Infrastructure)

These are data anchors. Low traffic individually but important for internal linking and LLM source coverage.

| Statute | What it covers | Priority |
|---|---|---|
| 316.193 | Main DUI statute | HIGH (covered above) |
| 316.1939 | Refusal to submit to testing | HIGH (combined with refusal situational page) |
| 316.1935 | DUI causing serious bodily injury/death | MEDIUM (feasibility check needed) |
| 322.34 | Driving with suspended/revoked license | MEDIUM (top DUI co-charge) |
| 322.2616 | Administrative license suspension | MEDIUM (the 10-day rule) |
| 843.02 | Resisting officer without violence | LOW (co-charge, but may not warrant standalone) |
| 948.01 | Probation / Adjudication Withheld | LOW for DUI (2.1% AW), HIGH for future charges |

---

## Template Transferability to Other Charges

The page structure above is designed to transfer. For Battery (next charge type), the template shifts:

| DUI Element | Battery Equivalent | Key Difference |
|---|---|---|
| 93% conviction rate | 54% conviction, 21% AW | AW explanation becomes primary content |
| Sentencing variance focus | Disposition variance focus | Different data story |
| Refusal situational page | Domestic violence indicator page | Different situational modifier |
| Diversion at 1.6% | Diversion at 18.3% | Diversion becomes much bigger story |
| Financial burden | Financial burden | Same structure |
| County interactive | County interactive | Same structure |
| Booking artifact analysis | Same analysis needed | Same methodology |

The core template — BLUF, realistic outcomes with interpretation, financial burden, non-conviction pathways, county interactive, co-occurring charges, next steps — transfers to every charge type. What populates each section changes. What sits in position 2 vs position 5 changes based on which data element carries the most reader benefit for that charge. But the structure is reusable.

---

## What's NOT Being Built (Phase 1)

- Synthesis pages (cross-county variance analysis, temporal trends) — Phase 1B or Phase 2
- Contributor sections — Phase 2+ (schema connection points built, empty at launch)
- 50-state transparency audit — Phase 2
- Cross-charge synthesis — Phase 2
- Non-DUI charge pages — after DUI template is validated
- API / data downloads — Phase 2+

---

## Next Steps To Build

1. Define the data queries needed to populate each section of each page (most already done, some gaps like DUI-with-injury feasibility, diversion program research)
2. Create the information sequencing for the charge hub page — section by section content draft with data placeholders
3. Define schema structure for the charge hub (the most complex page)
4. Build prototype of one page — likely the charge hub — with real data
5. Validate against V5's four pillars and priority stack
6. Extend template to first situational page (likely First DUI or Refusal)
