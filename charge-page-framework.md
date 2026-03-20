# Charge Page Framework: Block Library & Situational Discovery

**Date:** March 20, 2026
**Status:** Working framework derived from DUI calibration exercise. Represents current best thinking. Explicitly non-converged — every section marked with confidence level and expected change vectors. This is the map as we see it today, not the territory.

**How this document relates to other documents:**
- V5 checkpoint: governing architecture (pillars, pipeline, principles) — still canonical
- V5 working notes: data findings, corrections, competitive intelligence — ongoing
- DUI page architecture: specific DUI page map — first instantiation of this framework
- This document: the generalizable layer that should transfer across charge types

---

## Part 1: The Block Library

These are the modular content components that can appear on any charge page. Not every block appears on every page. Not every block has data behind it for every charge type. The library defines what each block IS, what question it answers, what data backs it, and where we currently see its availability.

**This list will grow.** As we profile additional charge types, new blocks will emerge that don't exist in DUI. Battery will likely surface a "protective orders / no-contact" block. Drug possession may surface a "quantity thresholds" block. The library is additive.

### Block 1: Statutory Explanation
**Answers:** "What am I charged with? What does this law actually say?"
**Source:** Statute text, plain-English translation
**Data required:** None (legal text)
**Availability:** Universal — every charge has a statute
**Schema:** LegalCode (unique to us, no competitor uses this)
**Notes:** This is infrastructure. Not the most read content but it anchors the page legally and serves LLMs seeking primary source text. Position varies — on statute pages it leads, on charge hubs and situational pages it's near the bottom.

### Block 2: Realistic Outcome Snapshot (BLUF)
**Answers:** "What's probably going to happen to me?"
**Source:** Disposition distribution from Clerk data
**Data required:** Disposition field (100% populated), filtered to charge type
**Availability:** Universal for any charge type in CJDT
**Notes:** The emotional anchor. For DUI this is "93% conviction" — sobering but honest. For marijuana possession this is "43% AW, 40% guilty" — a completely different story where AW explanation becomes critical. The BLUF framing changes based on which outcome category dominates. This is not one-size-fits-all text — it's charge-type-dependent editorial framing.

**Current thinking on how this varies by charge type:**
- High conviction charges (DUI 93%, Trespassing 77%): Lead with conviction reality, pivot to "what the sentence looks like"
- High AW charges (Marijuana 43%, Hit and Run 44%): Lead with "the most common outcome isn't what you think" — AW explanation becomes position 1
- High diversion charges (Battery 18%, Moving Traffic 16%): Lead with "there may be pathways that avoid this going on your record"
- Low conviction / high dismissal: Lead with the realistic range of outcomes

This is where editorial judgment per charge type matters most. Can't be templated — must be written per charge type based on what the data actually shows.

### Block 3: Sentencing Reality (With Interpretation)
**Answers:** "Am I going to jail? For how long? What's it going to be like?"
**Source:** SENTENCE_CONFINEMENT, MAXIMUM_TERM_DURATION_DAYS, CREDIT_TIME_SERVED, SENTENCE_PROBATION_DURATION_DAYS
**Data required:** Sentencing fields, jail classification metadata layer
**Availability:** Universal structure. The interpretation layer (booking artifact / real jail / mixed) needs to be built per charge type — the DUI classification may not transfer directly because different charge types may have different coding patterns.
**Notes:** This is our core differentiator. The raw jail percentage means nothing without the interpretation layer. For DUI we've built the full 42-county classification. For each new charge type, we need at minimum a statewide version of this analysis to know whether the same patterns apply.

**Open question:** Does the booking artifact pattern exist for non-DUI charges? Intuitively, it should — a person arrested for battery also spends a night in booking. But the pattern might differ because battery cases may involve longer pre-trial detention. We don't know yet. Each charge type needs its own classification pass.

### Block 4: Financial Burden
**Answers:** "How much is this going to cost me?"
**Source:** FINE + COURT_COST fields combined
**Data required:** Both fields populated (80% for DUI, varies by charge)
**Availability:** Depends on field coverage per charge type. Need to check per charge.
**Notes:** County-level variance is the value. Statutory fine ranges are on every attorney site. Actual median court-imposed totals by county are on nobody's site. The framing around "this is court costs only, here's what else you'll pay" is reusable across all charge types, though the specific add-on costs differ (DUI school vs anger management vs drug treatment, etc.).

### Block 5: Non-Conviction Pathways
**Answers:** "Can I avoid a conviction? What are my options?"
**Source:** Combined dismissal + diversion + AW + acquittal rates
**Data required:** Disposition field, county-level breakdown
**Availability:** Universal — but the WEIGHT of this block varies enormously. For DUI (6.6% non-conviction statewide) this is a minor section. For Battery (18% diversion alone) this is a major section. For Orange County DUI (41% non-conviction) this is THE story.
**Notes:** County-specific diversion program information is a research layer on top of the data. The data tells us the diversion RATE. Research tells us the program NAME, eligibility criteria, and what it involves. Both layers needed for full reader benefit.

**Open question:** How much program research is feasible at scale? For DUI in major counties we found RIDR (Hillsborough) and DROP (Pinellas). For every charge type in every county, this is a research project. May need to be Phase 2 or contributor-sourced.

### Block 6: AW Explanation
**Answers:** "What does 'adjudication withheld' mean? Is it a conviction? What does it mean for my record?"
**Source:** Educational content + disposition data
**Data required:** AW rate from disposition field
**Availability:** Universal — but only surfaces as a prominent block where AW rate exceeds ~10%
**Notes:** This is one of the most valuable content elements across the platform. AW is a Florida-specific legal concept that confuses everyone. 13 of the top 15 charge types have AW >10%. For marijuana possession and hit-and-run, AW is the MOST COMMON outcome. Every other legal site either ignores AW or gives a one-line definition. We explain it in context of the reader's charge type, with the actual probability of receiving it in their county.

The AW explanation content is largely reusable across charge types (the legal mechanism is the same). What changes per charge type is the statistical context and what AW specifically means for THAT charge (e.g., AW on a DUI still triggers license suspension, AW on battery may still trigger firearm restrictions).

### Block 7: County Interactive Element
**Answers:** "What about MY county specifically?"
**Source:** All metrics, county-filtered
**Data required:** Sufficient county-level volume per charge type
**Availability:** Depends on charge type volume and county coverage. DUI has 41 counties with good data. Smaller charge types may only have 15-20.
**Notes:** The structure is universal. The content within it is charge-specific. The interpretation layer (jail classification) is charge-specific. The threshold rules (when to show, when to caveat, when to suppress) transfer.

### Block 8: Circumstance Modifier
**Answers:** Charge-specific. "I refused the breathalyzer." "It was a domestic violence situation." "I only had marijuana." "It was shoplifting." "It was my first time."
**Source:** Varies — statute subsection, DOMESTIC_VIOLENCE_INDICATOR, DRUG_TYPE_DESC, Level/Degree field, MDM_PERSON_ID
**Data required:** Depends on the modifier — some are clean filters, some are partial, some are statutory-only
**Availability:** Charge-specific. This is where each charge type's situational pages come from.
**Notes:** This is NOT a single block. It's a category of blocks, each unique to a charge type. The DUI circumstance modifiers (refusal, BAC level, injury, minor in vehicle) are completely different from the battery modifiers (DV flag, severity of injury, weapon involvement, protective order violation). The block library expands per charge type as we profile each one.

### Block 9: Co-Occurring Charges
**Answers:** "What else am I facing? What charges come with this?"
**Source:** UNIQUE_CORRELATION_ID co-occurrence analysis
**Data required:** Co-occurrence query per charge type
**Availability:** Universal — works for any charge type
**Notes:** More relevant for some charges than others. DUI frequently co-occurs with refusal, suspended license, resisting. Battery frequently co-occurs with resisting, criminal mischief, violation of protective order. Drug possession co-occurs with drug equipment, driving offenses. The co-occurrence list serves two purposes: (1) alerts the reader to charges they may not know they're facing, (2) internal linking to related charge pages.

### Block 10: Procedural Next Steps
**Answers:** "What do I do RIGHT NOW?"
**Source:** Non-data. Statutory requirements, administrative procedures, practical guidance.
**Data required:** None
**Availability:** Universal structure, charge-specific content
**Notes:** For DUI, the 10-day DHSMV hearing rule is time-critical and almost nobody knows about it. Every charge type has equivalent time-sensitive procedural steps. This block is always near the end of the page (reader needs emotional anchoring before they can process procedural steps) but its content is critical. Contributor placement naturally fits here — the attorney is the person who helps you navigate these steps.

### Block 11: Attorney Representation Context
**Answers:** "Should I get a lawyer? Does it matter?"
**Source:** COUNSEL_CATEGORY outcome comparison
**Data required:** COUNSEL_CATEGORY field (60% county coverage, varies)
**Availability:** Available where data supports. Always requires heavy confounding disclosure.
**Notes:** Most commercially sensitive block. Must be handled with extreme methodological care. Never framed as "private attorneys get better outcomes" — always framed as "outcomes differ by representation type, which may reflect differences in case characteristics rather than attorney quality." This block may end up being more useful at the platform level (a synthesis page about representation) than at the per-charge-page level. Not converged.

---

## Part 2: Situational Page Discovery Process

### The Principle

A situational page exists when a person in a specific sub-situation would be poorly served by the hub charge page. The test is: **does this person need fundamentally different information, or just filtered information?**

If they need different information (different blocks, different priorities, different procedural steps): standalone situational page.
If they just need the same information filtered to their subset: the hub page's interactive element handles it.

### The Discovery Process Per Charge Type

**Step 1: Identify the dimensional splits.** What are the axes along which this charge creates different reader situations?

Common dimensions (apply to most charges):
- First vs repeat offense
- Misdemeanor vs felony severity
- County-level variance

Charge-specific dimensions (discovered per charge type):
- DUI: refusal, BAC level, injury, minor in vehicle
- Battery: DV flag, weapon, injury severity, protective order
- Drug possession: drug type, quantity, intent vs simple possession
- Theft: value threshold, retail vs non-retail, employee theft
- [Others discovered during profiling]

**Step 2: For each dimension, assess data filterability.**

| Filterability | Meaning | Example |
|---|---|---|
| Clean filter | A field in the data isolates this sub-population reliably | Level = 'Felony', DOMESTIC_VIOLENCE_INDICATOR = True |
| Partial filter | A field exists but has gaps or requires caveats | MDM_PERSON_ID for first offense, DRUG_TYPE_DESC at 6% |
| Statute-derivable | The statute subsection identifies the situation but the subsection field is patchy | DUI with injury = 316.193(3)(c), subsection field 43% |
| Not filterable | No field in the data isolates this population | BAC level, whether stop was legal |

Clean and partial filters → data-driven situational page.
Statute-derivable → try the filter, if sufficient volume proceed, if not → statutory/procedural page with hub-level data.
Not filterable → statutory/procedural page only. Still worth building if high-intent search query.

**Step 3: For each viable situational page, determine block assembly.**

Which blocks go on this page? In what order? The governing question: what does THIS reader need FIRST?

The block order is driven by the reader's emotional state and primary question, which differs by situation:

| Situation | Primary emotion | Leads with block | Secondary |
|---|---|---|---|
| First offense (any charge) | Fear of unknown | Pathways (hope) | Sentencing reality |
| Repeat offense | Fear of escalation | Sentencing reality (honest about escalation) | What's different this time |
| Felony | Fear of prison | Sentencing reality (prison data) | Long-term consequences |
| DV battery | Fear + relationship complexity | Procedural (no-contact, custody) | Outcome reality |
| Drug possession (small amount) | Embarrassment, fear for record | Pathways + AW explanation | Financial burden |
| Refusal / specific circumstance | Anxiety about that specific decision | Circumstance-specific outcome data | General charge outcomes |

This table is illustrative, not prescriptive. The actual block order for each page should be derived from first-principles reader analysis, not from a lookup table. Different charge types and situations will surface priorities we haven't anticipated.

**Step 4: The "does this page need to exist" test.**

Run each candidate through:
1. Is the reader in this situation poorly served by the hub page? (If the hub covers it, no page needed)
2. Is there search intent for this situation? (People actually look for this)
3. Do we have data OR substantive non-data content to offer? (At least statutory/procedural, ideally data)
4. Is the information different enough from the hub to avoid duplication? (Different blocks leading, different data, different priorities)

All four → build the page.
2-3 of four → candidate, evaluate after hub is built.
<2 → don't build, hub handles it.

---

## Part 3: Charge Type Profiles — Current State

### What we know so far from the expansion profiling query (2023-2025 data):

**Profiled with disposition, volume, AW rate, statute mapping complexity, counsel coverage:**

| Charge Type | Cases | Conviction | AW | Diversion | Dismissed | Statute Mapping | Discovery Status |
|---|---|---|---|---|---|---|---|
| DUI | 56,684 | 91.4% | 2.2% | 4.0% | 1.1% | Clean (316.193) | DEEP (full calibration complete) |
| Battery | 73,825 | 54.2% | 21.2% | 18.3% | 2.9% | Messy (31 strings) | SURFACE (profiled, not explored) |
| Drug Possession | 54,517 | 71.4% | 20.1% | 5.6% | 1.7% | Messy (25 strings) | SURFACE |
| Drug Equipment | 52,313 | 78.3% | 16.0% | 4.1% | 1.0% | Messy (11 strings) | SURFACE |
| Larceny | 109,998 | 63.7% | 20.2% | 13.6% | 1.6% | Messy (101 strings) | SURFACE |
| Trespassing | 63,306 | 76.8% | 13.0% | 3.3% | 4.2% | Messy (38 strings) | SURFACE |
| Resist Officer | 49,392 | 68.8% | 19.6% | 7.9% | 1.9% | Messy (34 strings) | SURFACE |
| Marijuana Possess | 19,375 | 40.3% | 43.1% | 14.2% | 1.9% | Messy (10 strings) | SURFACE |
| Hit and Run | 18,399 | 41.4% | 43.6% | 12.8% | 1.7% | Messy (11 strings) | SURFACE |
| Burglary | 16,367 | 74.1% | 16.2% | 4.0% | 1.8% | Messy (19 strings) | SURFACE |

### What we DON'T know yet for non-DUI charge types:

- Sentencing patterns and whether the booking artifact issue exists
- County-level variance on any metric
- Financial burden field coverage
- Co-occurrence patterns
- Which situational dimensions are filterable from the data
- Whether the DV indicator is useful for battery (63% populated — promising but unvalidated)
- Whether DRUG_TYPE_DESC at 6% is useful for anything
- Charge-to-statute mapping decisions (FCIC category vs statute wildcard for each)

### Anticipated per-charge-type profiling needs:

For each charge type we decide to build, we need a lighter version of the DUI calibration:
1. Filter definition (FCIC or statute? Document the choice)
2. Disposition distribution statewide and by county
3. Sentencing distribution + booking artifact check (at least statewide)
4. Financial burden field coverage
5. Situational dimension inventory (what fields filter what sub-populations)
6. Co-occurrence analysis
7. Any charge-specific data fields that apply (DV indicator for battery, drug type for drugs)

This is a few hours of Manus queries per charge type, not the weeks-long DUI deep dive. We already know the data structure. We're just running the same analysis pipeline on a different filter.

---

## Part 4: Situational Page Candidates By Charge Type

**Confidence level: SPECULATIVE.** These are best-guess candidates based on general legal knowledge and the data dimensions we've identified. The actual situational page inventory for each charge type won't be confirmed until we profile the data and apply the discovery process from Part 2.

### DUI (316.193) — CONFIRMED situational pages:
- First DUI in Florida ✓
- Second/Repeat DUI ✓
- Felony DUI ✓
- DUI Refusal ✓
- DUI with Injury (statutory + felony data)
- Potentially: DUI with minor in vehicle, DUI commercial driver (if statute subsection supports)

### Battery (784.03) — PROBABLE situational pages:
- Domestic violence battery (DV indicator field, clean filter where populated, completely different procedural reality — mandatory arrest, no-contact orders, child custody implications)
- Aggravated battery (784.045, separate statute, felony — clean filter)
- First offense battery (MDM_PERSON_ID, same methodology as DUI)
- Battery with diversion (18.3% diversion rate — which counties? What programs? This is a big story for battery defendants)
- Potentially: battery on law enforcement (severity escalation), battery on elderly/disabled

### Drug Possession (893.13) — PROBABLE situational pages:
- Marijuana possession specifically (FCIC splits this out, 19K cases, 43% AW — radically different outcome profile from other drugs)
- Possession with intent to distribute (severity escalation, likely identifiable via statute subsection or Level field)
- First offense drug possession (diversion is common for first-time drug offenses)
- Potentially: possession of specific drug types if DRUG_TYPE_DESC has sufficient coverage for cocaine, meth, etc. (currently 6% populated — probably insufficient)

### Larceny/Theft (812.014) — PROBABLE situational pages:
- Petit theft vs grand theft (value threshold, misdemeanor vs felony — likely identifiable via Level field)
- Retail theft / shoplifting (extremely common specific situation, may be identifiable via statute subsection)
- First offense theft (diversion programs)
- Employee theft (statute subsection, likely small N)

### Resist Officer (843.02) — PROBABLE situational pages:
- With violence vs without violence (843.01 vs 843.02, different statutes, clean split)
- As a co-charge vs standalone (the reader's situation is different if this is their only charge vs an add-on to DUI/battery)

### Burglary (810.02) — PROBABLE situational pages:
- Occupied vs unoccupied structure (different severity, statute subsections)
- Burglary of dwelling vs commercial (different penalties)
- Armed burglary (severity escalation)

### Hit and Run (316.061/316.063) — PROBABLE situational pages:
- Property damage only vs injury involved (different severity)
- The 43.6% AW rate makes this a very different story than most charges — AW is THE outcome here

### Others — INSUFFICIENT INFORMATION:
For Moving Traffic, Nonmoving Traffic, County Ordinance, Municipal Ordinance, Drug Equipment, Trespassing, Criminal Mischief: we don't have enough insight yet to speculate on situational pages. These need profiling first.

---

## Part 5: What We Expect To Change

This section explicitly catalogs what we think is likely to shift as we move from DUI into other charge types.

**The interpretation layer may work differently.** The booking artifact pattern was the defining insight for DUI. For battery, the defining insight might be something else entirely — maybe the DV indicator creates a bigger split than county variance. For drug possession, it might be the marijuana/non-marijuana split. Each charge type will likely have its own "the number doesn't mean what you think it means" discovery.

**Block priority order will vary more than expected.** We've mapped some initial heuristics (first offense → pathways lead, felony → sentencing leads) but real data may show that some charge types don't follow these patterns. A first-offense drug possession defendant may actually need the procedural block first (drug court eligibility has enrollment deadlines similar to DUI's 10-day rule).

**Some charge types may not warrant a full hub page.** Drug Equipment Possession (52K cases) almost always co-occurs with Drug Possession. The reader charged with both needs one page that covers both, not two separate hubs. The charge types that are primarily co-charges rather than standalone charges may function better as sections within the primary charge's hub.

**Statute mapping decisions will be hard.** DUI was the clean case — one statute, one charge. Battery has 31 statute strings. Larceny has 101. For each, we need to decide: use FCIC category (accept clerk misclassification noise) or define a statute filter (accept gaps). This decision materially affects what data appears on the page and needs to be made per charge type, documented, and defensible.

**County-level data quality issues will differ per charge type.** Miami-Dade's misdemeanor DUI gap is confirmed. But they submit felony cases normally. A charge type that skews felony (burglary, aggravated battery) may have good Miami-Dade data. A charge type that skews misdemeanor (petit theft, simple battery) may have the same gap. We can't assume the DUI data quality profile transfers.

**New blocks will emerge.** Battery will likely need a "protective orders and no-contact" block that doesn't exist in the current library. Drug charges may need a "drug court and treatment" block. Theft may need a "restitution" block. The block library is designed to grow.

**The reader emotional model may need refinement.** We've been working from V5's reader models (stressed person at 2 AM, scanning on mobile). This probably applies well to DUI and battery (arrest-driven). It may apply differently to theft (might be charged via summons, not arrest), drug possession (varies by severity), or traffic violations (usually a citation, not an arrest). The emotional state drives block order, so getting it right per charge type matters.

---

## Part 6: The Pipeline Going Forward

### For each new charge type, the process is:

1. **Profile the data** (disposition, sentencing, financial coverage, county variance, field-specific checks) — Manus queries, a few hours
2. **Identify the editorial story** — what does this charge type's data say that's surprising, useful, or different from what people expect? This is the equivalent of DUI's "93% conviction but the jail rate is misleading" finding.
3. **Discover situational dimensions** — which fields create meaningful sub-populations? Which are filterable? Which matter to the reader?
4. **Map the block assembly** — for the hub page and each situational page candidate, which blocks in what order?
5. **Apply the "does this page need to exist" test** — from Part 2 above
6. **Build** — content with data placeholders, then populate

### What we're NOT doing:

- We're not building 4,500 programmatic pages
- We're not deciding the full page inventory before profiling the data
- We're not assuming the DUI template transfers without modification
- We're not treating the block library as closed
- We're not committing to page designs before understanding each charge type's data story
- We're not optimizing for search volume — we're optimizing for reader benefit in genuine situations

### What we ARE doing:

- Building a reusable analytical pipeline (data profiling → editorial discovery → situational mapping → block assembly)
- Maintaining a growing block library that accumulates capability
- Treating each charge type as its own editorial exercise within a shared framework
- Letting the data tell us what's interesting and useful, not deciding in advance
- Keeping the interpretation layer as the core differentiator everywhere
