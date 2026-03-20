# Legal Data Synthesis Platform: Project Checkpoint v5

## Document Purpose

This document is a self-contained checkpoint capturing the full state of a project in active development. It is designed to be consumed by an LLM or human collaborator with zero prior context. All terminology is defined on first use. All reasoning is made explicit. All architectural decisions include the reasoning chain that produced them. No external references are required.

This document consolidates all prior work: v4 checkpoint, four amendments (E-E-A-T timeline and priority stack; research framework integration; structural pillar framework and reader models; page architecture restructuring), working notes (paradigm corrections, reasoning chains, implementation notes), a SWOT analysis, a multi-source data framework, and a data journalism pipeline reframe. Prior versions are fully superseded.

**Date:** March 18, 2026
**Version:** 5
**Status:** Phase 1A ready to execute. Florida confirmed as proof-of-synthesis jurisdiction. Direct competitor (FloridaCourtFile.com) identified and analyzed. AI citation opportunity confirmed as open. Governing architectural framework (four pillars, five page types, data journalism pipeline) established.

**How to read this document:** Sections 1-3 establish the governing framework (terminal objective, pillar architecture, constraints). All subsequent sections are downstream of this framework. When a decision is made later in the document, the pillar reasoning is referenced. If something seems arbitrary, check whether the pillar framework explains it -- it almost certainly does.

---

## Evidence Classification System

**[CONFIRMED]** -- Direct evidence exists. Data downloaded and inspected, source code viewed, claim verified firsthand during this project's research cycle.

**[LOGICALLY DEDUCED]** -- Follows from strong reasoning applied to confirmed or reported evidence. The reasoning is sound but the conclusion could be wrong if underlying assumptions are incorrect.

**[UNVERIFIED]** -- Plausible and worth considering but no direct evidence yet. May be based on industry framing, analogical reasoning, or third-party assertions not independently confirmed.

**[REPORTED]** -- Finding from published third-party research (SimilarWeb, Ahrefs, Pew Research, etc.). Cited with source where relevant.

When a tag appears, it applies to the specific claim it is attached to, not the entire paragraph.

---

## Key Terminology

**Information Gain:** A concept from information theory measuring how much genuinely new information a document introduces relative to the existing indexed corpus. Search engines and AI models use this as a ranking and citation signal. Content with zero information gain is algorithmically suppressed. [LOGICALLY DEDUCED -- well-documented in SEO research; specific algorithmic implementation is industry consensus.]

**Net New:** Data, statistics, or analytical findings that did not previously exist in consolidated, published form on the public internet. As of March 2026, basic county-level disposition statistics from Florida's CJDT dataset are no longer net-new (FloridaCourtFile.com publishes them). Net-new for this project comes from synthesis, cross-references, editorial quality, contextual analysis, and multi-source data combinations that programmatic templates cannot produce.

**Empirical Alchemy:** Creating original, proprietary statistics by combining fragmented public data sources. The practitioner synthesizes data points that did not exist before by cross-referencing independent sources. The more sources cross-referenced, the more novel and irreplicable the findings.

**Data Synthesis:** The core activity. Taking two or more independent data sources, normalizing them into comparable formats, and cross-referencing them to produce metrics or findings that neither source contains individually.

**Data Harmonization:** Distinct from normalization. Normalization standardizes terms within a single dataset (mapping Florida's "Adjudication Withheld" to a standard category). Harmonization aligns two different datasets that measure related but not identical things (cross-referencing court disposition data with administrative license suspension data). Harmonization is the harder problem -- forcing alignment between systems that weren't designed to communicate.

**EDA (Exploratory Data Analysis):** The private testing stage where cross-references are validated before publication. Every data combination is plotted and examined internally before any finding reaches a public page. If numbers don't make sense (dispositions exceeding arrests for a county, implausible correlations), the linkage is broken and the cross-reference is killed. This stage is the credibility protection mechanism.

**Editorial Triage:** The publish/kill decision applied at the data analysis stage, not the page stage. A cross-reference that is technically valid but reveals nothing meaningful (the Dead Man's Zone) is killed here. A cross-reference that reveals a meaningful finding proceeds to documentation and publication.

**Data Provenance / Epistemological Transparency:** The practice of explicitly documenting the origin of data, the transformations applied to it, and the known flaws, gaps, or limitations. Following the Our World in Data model: exhaustive methodological transparency. The finding is the headline. The methodology is the credibility.

**Visual Encoding:** The translation of normalized numbers into visual properties (length, position, color) following information design principles. Distinct from "charting" -- informed by Edward Tufte's principle of maximizing the data-ink ratio (showing the data) and minimizing chartjunk (visual fluff that distracts). One chart, one finding, one dimension.

**Progressive Enhancement:** A web design principle where the base page works without JavaScript. JavaScript makes it better but isn't required. Applied to the interactive county data element: all county data is pre-rendered in the HTML (crawlable, accessible). JavaScript collapses it into the interactive selector for capable browsers. The page never breaks.

**Tier A/B/C Data:** Tier A: free, programmatic, commodity-level (statute text, penalty ranges -- every legal site has this). Tier B: paid or labor-intensive, high-differentiation (court disposition outcomes, timelines, charge co-occurrence -- the synthesis layer). Tier C: contributor-sourced, irreplicable (practitioner knowledge from attorneys -- typical plea offers, courtroom procedures, local defense strategies).

**Structural Hole:** A gap in information flow between isolated knowledge clusters (Ronald Burt). Value is created by brokering information across these gaps. The structural holes exist between isolated data systems (court records, statute databases, DMV records, arrest data, sentencing data) that describe different dimensions of the same legal reality but have never been connected. [CONFIRMED -- competitive landscape audit verified no entity bridges these systems at the consumer-facing synthesis level.]

**Citation Lock-in:** A compounding temporal advantage where, once established as the canonical source for a data point, displacement becomes progressively harder as each citation reinforces authority. This is a temporal advantage, not a structural barrier to entry.

**Information Sequencing:** The order in which information is presented, derived from Jobs-to-be-Done analysis: (1) what the charge means, (2) what typically happens in practice, (3) what makes it beatable, (4) related charges, (5) what to do next, (6) full legal detail last. This inverts legal content convention (which leads with maximum penalties) because the reader's primary need under stress is realistic outcome information, not statutory maximums. [LOGICALLY DEDUCED -- JTBD-derived but untested with actual users.]

**Entity Salience:** The prominence and clarity with which recognized entities are defined and related within a document. High entity salience signals a primary source.

**Dead Man's Zone:** Content between high-value atomic pages and high-value meta-synthesis that serves no clear audience and generates no information gain. Generic comparisons confirming expected patterns. Must be avoided.

**AI Overview:** Google's generative search feature synthesizing answers directly on the SERP. Appears on approximately 60%+ of all queries and 23-78% of legal queries depending on type. [REPORTED] Being cited in AI Overviews is a primary distribution mechanism.

**Schema Markup:** Structured data in JSON-LD format within page source code telling machines what content represents. Relevant types: Dataset, StatisticalVariable, FAQPage, LegalCode, Article, Person, Organization, BreadcrumbList, DefinedTerm, ClaimReview, DataCatalog.

**BLUF (Bottom Line Up Front):** Each content section opens with a direct answer (40-50 words). [REPORTED -- 55% of AI Overview citations come from the first 30% of page content.]

**Zero-Click Economy:** ~83% of informational searches terminate on the SERP without an outbound click. [REPORTED] AI citation is the distribution mechanism. Clicks that occur represent disproportionately high-intent users.

**Content Neutrality:** All published data is statistical reporting without editorial interpretation. The project reports what data shows, documents methodology, acknowledges limitations. It does not advocate, critique, or frame variance as misconduct.

**Confounding Variable Disclosure:** Any cross-reference involving demographic or representation-type variables must include explicit acknowledgment of uncontrolled variables (pre-trial detention status, charge severity, prior record, indigency). Statistical integrity requirement, not political caution.

**FloridaCourtFile.com (FCF):** Closest direct competitor. Launched March 8, 2026 by CourtFile LLC. 4,502 programmatic CJDT data pages (67 counties × 36 charge types). Lead-generation model. Best-in-class Dataset + FAQPage schema. #1 organic rankings for long-tail queries. Zero AI Overview citations. No synthesis, no editorial depth, no named experts, no Tier C, zero backlinks. [CONFIRMED]

**Domain Sandbox:** Evaluation period where new YMYL domains have schema indexed but aren't trusted by AI Overviews for citation. FCF's zero-citation result despite #1 organic rankings and perfect schema is the empirical reference. [CONFIRMED]

**Jurisdiction Accessibility Tiers:** Tier A: full data richness, bulk download, statewide coverage. Tier B: partial data, formal request or paid subscription. Tier C: fragmented or expensive, commercial APIs or FOIA. Data accessibility and commercial priority are independent dimensions.

**Claim-Evidence Architecture:** Every statistical claim within a content block is paired with its evidence (source, date range, sample size, critical caveats) within that same block. An LLM extracting a single block gets the claim and enough evidence to verify without needing to retrieve a separate methodology section.

**RAG-Optimized Semantic Chunking:** Content structured into 200-400 word self-contained blocks, each independently retrievable by a RAG pipeline without needing surrounding context. Reader Benefit determines block boundaries; the word range is a calibration target, not a rigid rule.

---

## Section 1: Terminal Objective and Goal Stack

### Goal Stack Decomposition

| Level | Goal | Type |
|---|---|---|
| Surface | Build a legal statute directory for Florida | Proxy |
| Level 2 | Be the most comprehensive legal data reference | Proxy |
| Level 3 | Be the data source AI systems cite for legal queries | Proxy |
| Level 4 | Build a canonical citation source for regulatory outcome data that compounds over time | Proxy |
| Level 5 | Build a domain-agnostic data synthesis engine where legal is the first payload | Proxy |
| Terminal | Create a self-reinforcing data synthesis platform that becomes the canonical cited source for regulatory outcome data, where each data point, citation, and jurisdiction compounds the value of every other, and the architecture transfers to any domain with fragmented public data and structural holes | Terminal |

### Why the Terminal Objective Determines Everything

If the goal were "rank for Florida DUI keywords," SEO would be the primary structural concern. If it were "generate attorney lead revenue," conversion optimization would dominate. Neither is the goal.

The goal is canonical citation authority on a compounding, transferable platform. This makes certain things structural that would otherwise be augmentation (system coherence, architectural transferability) and makes certain things augmentation that would otherwise seem structural (traffic volume, conversion rate, competitive ranking position).

The legal vertical is the first instantiation, not the destination. The four-tier hierarchy, the data pipeline, the schema strategy, the editorial gate, and the authority-building approach all transfer to any domain where fragmented public data can be synthesized into net-new findings. Healthcare regulations (treatment outcomes by facility), financial regulations (enforcement actions by agency), tax code (audit rates by jurisdiction), building codes (inspection outcomes by municipality), environmental compliance (violation data by facility). Each vertical follows the same pattern: fragmented public data, structural holes between data systems, nobody synthesizing it consumer-facing. The pipeline is the product. Everything else is an expertise payload.

---

## Section 2: The Four Pillars

Every content, data, and architectural decision in this project is governed by four structural pillars derived from four independent, irreducible failure modes.

### The Four Failure Modes

**Failure Mode 1: Wrong Question.** A technically excellent page -- perfectly structured, perfectly schema-marked, perfectly novel -- but it answers the wrong question. The person charged with DUI can't find what they actually need. The page is built around what the data can show rather than what the reader needs to know.

Independence test: Can this fail while data is correct, machines can parse it, and the system is coherent? Yes. A perfectly correct, machine-readable, system-coherent page that answers the wrong question is useless.

**Failure Mode 2: Data Falsehood.** Pages are well-structured for humans and machines, but the underlying data is wrong. Normalization errors, apples-to-oranges comparisons, confounding variables unacknowledged, sample sizes too small. One journalist catches an error and credibility is permanently destroyed.

Independence test: Yes. A perfectly structured, machine-readable, system-coherent page with wrong data is a liability.

**Failure Mode 3: Machine Invisibility.** Pages perfectly serve the reader but an LLM can't parse the data with enough confidence to cite it. No schema, no structured claims, no machine-verifiable provenance chain. Invisible to the distribution mechanism.

Independence test: Yes. A page that perfectly helps every human who finds it but that no LLM can cite fails against the terminal objective.

**Failure Mode 4: System Incoherence.** Each individual page is correct, helpful, and machine-readable. But the system contradicts itself. Tier 2 statewide averages don't match Tier 1 county sums. Schema chains are broken. An LLM crawling multiple pages finds contradictions and downgrades trust in the entire domain.

Independence test: Yes. A collection of individually excellent pages that contradict each other is a trust failure.

### The Four Pillars

**Pillar 1: Reader Benefit.** Does this page genuinely help the specific human who lands on it, given their cognitive state, their actual question, and their real-world situation? Gates everything. Most upstream. The page answers what the reader needs, in the order they need it, with information that respects their intelligence. Equally important: the page excludes information that doesn't serve this reader at this tier.

**Pillar 2: Data Truthfulness.** Is the underlying data correct, the methodology sound, the comparisons valid, and the limitations honestly disclosed? Every claim verifiable. Normalization documented. Confounders disclosed. Sample sizes stated. No claim exceeds what the data supports. Gates Machine Confidence (making incorrect data machine-readable accelerates error distribution).

**Pillar 3: Machine Confidence.** Can an LLM parse this page, trust the data, verify its provenance, and cite it with confidence? Schema validates. Claims paired with inline evidence. Provenance chain explicit. Entity relationships machine-readable. Each section independently retrievable. Downstream of Pillars 1 and 2.

**Pillar 4: System Coherence.** Do the pieces connect correctly across tiers, time, and jurisdictions? Data updates propagate. Schema chains intact. Cross-tier aggregations mathematically consistent. Parallel to the sequential chain. Augmentation at Phase 1 scale. Transitions to structural at Phase 2+ scale.

### Dependency Ordering

```
Reader Benefit → Data Truthfulness → Machine Confidence
                                                        } System Coherence (parallel)
```

Reader Benefit gates Data Truthfulness (rigorous methodology on the wrong analysis is wasted effort). Data Truthfulness gates Machine Confidence (making wrong data machine-readable accelerates error distribution). Machine Confidence operates within the space the first two define.

**Decision Resolution Rule:** When pillars conflict, the upstream pillar wins:
1. Reader Benefit overrides all. Data that doesn't serve the reader at this tier doesn't appear on this tier's pages, regardless of Machine Confidence value.
2. Data Truthfulness overrides Machine Confidence. Methodologically invalid comparisons don't get schema-marked, regardless of citability.
3. Machine Confidence optimizes within the space defined by the first two.
4. System Coherence constrains all three at scale.

### The Priority Stack

For all page-level content decisions:

**Priority 1: Serve reader intent.** Every element evaluated against: what is the person landing here actually looking for? What genuinely helps? What are the second-order consequences they haven't considered? What is NOT helpful and should be excluded?

**Priority 2: LLM-readable and genuinely helpful to the machine.** Structure so an LLM reads with full confidence. Correct schema, cited sources, verifiable data, semantic entity mapping. The LLM determines: this data is real, this source is trustworthy, I can cite this.

**Priority 3: Net-new / citable.** Can we synthesize something that doesn't exist elsewhere? This is the aspiration layer. But it is third, not first. A page that serves the reader and is fully LLM-readable publishes even without a net-new element (at Tier 1-2). A page with a net-new element that doesn't serve the reader does not publish.

### Tension Topology

**Reader Benefit ↔ Machine Confidence (Medium tension):** Reader Benefit wants natural, flowing content for humans under stress. Machine Confidence wants discrete semantic blocks and schema annotation. Resolution: the BLUF serves both (the snippet the LLM extracts IS the answer the reader needs). When they diverge, data moves to the invisible schema layer, not the visible content layer.

**Reader Benefit ↔ Data Truthfulness (Low tension):** Reader Benefit wants clear answers. Data Truthfulness wants caveats. Resolution: progressive disclosure. BLUF gives the answer. Caveats exist below the scan-stop point or in linked methodology. Both pillars satisfied.

**System Coherence ↔ All (Currently low, grows with scale):** At Phase 1, few pages, easy to maintain manually. At Phase 2+, every page-level decision can create system-level inconsistency. Design coherence rules now. Enforce at scale.

---

## Section 3: Constraint Landscape

### Hard Constraints (Cannot Be Violated)

| Constraint | Organic/Synthetic | Reasoning |
|---|---|---|
| Data must be factually correct | Organic | One wrong number cited by an LLM traces back and the trust model collapses |
| Content neutrality -- no editorializing | Organic | Editorializing invites political backlash threatening data access. Court administrators can object to advocacy. They cannot object to neutral statistics. |
| Statistical integrity -- valid comparisons only | Organic | Misleading cross-references are worse than none. A flat comparison of public defender vs. private attorney outcomes without confounding disclosure is statistically invalid. |
| Legal framing as statistical reporting, not advice | Organic | Liability. The platform reports data. It does not advise. |

### Resource Constraints

| Constraint | Impact |
|---|---|
| Solo operator at launch | Limits production volume. Reinforces quality-over-quantity. |
| No attorney contributor at launch | E-E-A-T gap accepted. Schema connection points built but empty. Phase 2+. |
| No institutional credibility at launch | Built through data quality, schema, and Tier 4 authority. |

### Environmental Constraints

| Constraint | Organic/Synthetic | Reasoning |
|---|---|---|
| 83-88% zero-click environment | Organic | The empirical reality. Build for citation, not traffic. |
| Domain sandbox for new YMYL sites | Organic | Confirmed by FCF. Expected operating condition, not risk to mitigate. |
| FCF occupies basic CJDT statistics | Organic | Net-new threshold raised. Differentiation through synthesis, editorial quality, multi-source. |
| LLMs are the primary distribution mechanism | Organic | Distribution depends on machines citing, not humans finding via traditional search. |

### Self-Imposed Constraints (Highest Signal)

| Constraint | What It Reveals |
|---|---|
| Every page must genuinely serve the reader | Reader Benefit is the primary structural pillar |
| No performative empathy, no fear-mongering, no leading with max penalties | Quality standard: information that respects intelligence |
| 20 excellent pages over 50 adequate ones | The editorial gate is genuine, not a guideline |
| Epistemic honesty -- tag confidence, disclose limitations | Transparency is a value, not a tactic |
| The pipeline must transfer to the next domain | System coherence and transferability are structural |

---

## Section 4: Project Genesis and Strategic Evolution

### Original Concept

A legal statute reference platform: plain-English explanations of specific laws, enriched with data, monetized through attorney contributor placements. Six-layer page architecture. Reference model: Shouse Law Group.

**Corrected Shouse benchmark [REPORTED]:** SimilarWeb estimates Shouse at ~85,594 monthly visits (February 2026), declining 51% YoY. The previously cited 3.1M figure was not validated and is retired.

### Five Strategic Pivots

**Pivot 1: From "Legal Content Site" to "Data Synthesis Layer."** Build a data layer producing normalized court outcome statistics. The website is one interface. The data is the asset.

**Pivot 2: From "Page Traffic" to "Be the Source."** Success = being cited as the canonical source. Citation frequency, not page traffic, is the terminal metric. This is the trajectory, not the launch metric. Launch metric is structural citability. [REPORTED evidence:] Traffic bifurcation confirms: Justia (primary source, statute text) +11.4% YoY. Shouse (explanatory content) -51%. Nolo -42.3%. AI Overviews absorb explanatory content and cite primary sources. This project builds primary source data.

**Pivot 3: From "Programmatic Scale" to "Data-Driven Editorial Gate."** Only produce content where data earns its existence. The editorial gate is tiered: Tier 1 requires quality, structure, and reader benefit. Tier 2 expects net-new aggregation. Tier 3 mandates net-new with the full editorial gate.

**Pivot 4: From "County-Level Only" to "Cohort Aggregation."** Aggregated rural cohorts compared to metro cohorts. Standard social science methodology solving the sample size problem.

**Pivot 5: From "One Revenue Model" to "Multiple Interfaces on the Same Dataset."** Contributor placements primary. Data licensing, institutional subscriptions, analytics dashboards as Phase 2+ potentials. [UNVERIFIED for Phase 2+ paths.]

### The Appreciating Asset Thesis

A legal content site is a depreciating asset -- dependent on algorithmic stability, vulnerable to AI summarization. This project is designed as an appreciating asset. Data accumulates historical depth. Cross-references multiply with jurisdiction. Citation momentum compounds. Content depreciates. Data appreciates. Build data with a content interface, not content with data enrichment. [LOGICALLY DEDUCED]

### The Paradigm Shift: Old SEO vs. New SEO

This is the single most important context for any LLM working on this project.

**The old paradigm** measures success by monthly organic traffic. Content ranks for keywords. More visits = more value. Declining traffic = failing strategy. Under this paradigm, the decline in legal content traffic (Shouse -51%, Nolo -42%) would be alarming.

**The new paradigm** measures success by citation authority and canonical source status. Content is produced to be the data AI systems cite. Citation frequency is the metric. Being referenced in AI-generated answers = value, regardless of whether a click occurs.

Under this paradigm, the traffic decline is **validating**. AI Overviews absorb surface-level explanatory content -- exactly as predicted. The 83% who get answers from the AI Overview were never high-value visitors. The 17% who click through are self-selected for genuine need. Each click is worth dramatically more.

**Do not apply old-paradigm thinking to this project.** Specifically:
- Do not flag low monthly search volume for county-level data queries as a concern. The 930-3,340 explicit data queries is the tip. Every AI Overview answering a DUI question potentially cites this data.
- Do not treat declining traffic at competitor sites as evidence of a shrinking market. It's evidence of a shifting distribution mechanism favoring primary sources.
- Do not evaluate the contributor model primarily on click volume. The value is canonical source association.
- Do not suggest content designed to "capture traffic." The content must be genuinely net-new data structured for machine extraction. Discovery is through citation, not ranking.

### The Fractal Data Architecture

One normalized dataset renders at multiple zoom levels. You are not producing five different pieces of content. You are looking at the same data through five different lenses.

Zoom 1 (statute page): single county's DUI disposition distribution. Zoom 2 (charge page): all counties aggregated statewide with county breakdown. Zoom 3 (synthesis page): cross-county variance as a finding. Zoom 4 (cross-reference): disposition × second dimension (representation type, demographics). Zoom 5 (distribution asset): chart, summary, shareable format.

One data extraction. One normalization. Five outputs. Marginal cost of each additional zoom level is minimal. Each new data point entering at the atomic level automatically enriches every zoom level above.
## Section 5: Page Architecture

### The Core Insight

Pages are organized by how people search and what genuinely helps them, not by how the data is structured in the database.

The data lives at the county level in the database. Always. Every CJDT record has a COUNTY_DESCRIPTION field. This is a pipeline fact. But the primary page surface is state-level, organized by charge type and situation, because that's how people actually search and that's where sample sizes are robust.

County-level data is a feature within those pages, not a separate page. The reader who was charged in Orange County lands on "DUI in Florida," sees the statewide picture first (orientation, emotional relief, realistic outcome range), and drills into their county through an interactive element. They see their county in context of the state -- which is more useful than their county in isolation. "Orange County's conviction rate is 68% compared to the statewide average of 63%" tells them something. "68%" alone tells them nothing because they have no baseline.

This retires the assumption (inherited from FCF's model) that county-level data granularity requires county-level URLs. Tested against all four pillars:

- **Reader Benefit:** Most readers search by charge + state, not charge + county. The county comparison within a state page serves them better than an isolated county page.
- **Data Truthfulness:** State-level statistics are more robust (340K DUI records statewide). County-level stats for small counties may be misleadingly swingy.
- **Machine Confidence:** A state-level page with 340K records in its Dataset schema is a more confident citation source than a county page with 47 records.
- **System Coherence:** Fewer URLs to maintain consistency across. County data is a feature of the state page, not an independent entity that can drift out of sync.

### The Five Page Types

#### Page Type 1: Statute Reference Pages

One per statute per state. Example: "Florida Statute 316.193."

Data infrastructure. Organized by legal code (what's on citation paperwork). Contains: statute text with LegalCode schema, plain-English explanation, penalty structure, statewide disposition data, link to corresponding charge page(s). Serves: the narrow audience searching by statute code (charged person reading paperwork, attorneys, paralegals, LLMs seeking primary statute text).

Low traffic per page. Long-tail aggregate value across hundreds of statutes. These are data anchors referenced by charge pages and situational pages.

**Tier mapping:** Tier 1 (Collect). Raw material and data infrastructure.

#### Page Type 2: Charge Pages

One per charge type per state. Example: "DUI in Florida."

Primary discovery surface. Matches how the majority search (charge name + state). Contains: the full information sequencing (Section 8), statewide disposition data as BLUF, penalty tiers, AW explanation, county-level interactive element (Section 6), charge co-occurrence patterns, procedural timeline, links to situational pages, contributor space, methodology.

Highest traffic volume of any page type. The workhorse.

**Tier mapping:** Tier 2 (Serve). Reader-facing, designed around user intent.

#### Page Type 3: Situational Pages

One per common specific situation per state. Examples: "First Offense DUI Florida," "Felony DUI Florida," "DUI with Injury Florida."

Charge page variants filtered to a specific scenario. Match the highest-intent queries -- the person who knows their exact situation. Pull from the same database but scope to the reader's scenario: first-offense-only disposition data, felony-only outcomes. Follow the same information sequencing but filtered.

Content does NOT include information about other offense tiers. The first-offense reader doesn't need felony DUI information.

**Filtering feasibility caveat:** Not all situational filters produce clean subsets. "First offense" requires PERSON_ID lookup (see Section 14 for temporal scope mismatch). "Felony DUI" is a clean filter on the Level field. "DUI at checkpoint" may not be identifiable from CJDT fields. The set of viable situational pages is determined by what the data cleanly supports, not by what queries people search. Pages requiring assumptions to filter disclose the methodology or are not built. [Data Truthfulness gate.]

**Temporal scope mismatch for situational filtering:** The trailing window determines which cases appear in statistics. But the first-offense filter requires looking BACK across the full dataset to identify repeat offenders via PERSON_ID. A defendant with a 2019 DUI who gets a 2024 DUI appears in the trailing window but identifying them as repeat requires data outside the window. Two operations: (1) identify population across full dataset, (2) compute statistics on trailing window subset only. Required methodology disclosure: "First offense defined as no prior DUI charge for same individual in CJDT dataset (2018-present). Prior history before 2018 not available."

Potentially the most commercially valuable pages (most specific intent, closest to attorney engagement).

**Tier mapping:** Tier 2 (Serve). Same tier as charge pages, different data filter.

#### Page Type 4: County Pages (Conditional)

Only where three conditions are simultaneously met:

**Condition 1: Sufficient data volume.** Enough cases for the charge type within the trailing window to produce robust, non-swingy statistics. Threshold calibrated during Phase 1A from actual data variance. [Not converged.]

**Condition 2: Demonstrated search demand.** Evidence that people search for this county × charge combination at volume justifying a standalone page.

**Condition 3: Genuinely differentiated outcomes.** County's data meaningfully different from statewide average -- different enough that the divergence is informative. Threshold calibrated during Phase 1A. [Not converged.]

Expected count for Florida DUI: 5-10 counties at most (Miami-Dade, Broward, Hillsborough, Orange, Palm Beach, Duval, potentially others). Not 67. Not programmatic. Each earns its existence.

**Tier mapping:** Tier 2 (Serve). Same tier, geographic filter.

#### Page Type 5: Synthesis Pages

Only where the editorial gate is passed: intent exists, data says something meaningful, comparison structurally valid.

Examples: "How DUI Outcomes Vary Across Florida Counties," "DUI Disposition Trends in Florida: 2018-2025," "The Effect of Representation Type on DUI Outcomes."

Serves the Tier 3 reader: journalists, attorneys analyzing patterns, policy researchers, academics, reform advocates, LLMs seeking analytical data. Content follows the Tier 3 reader model (Section 7).

The full 56-county comparison table lives here. The detailed temporal trend analysis lives here. The demographic cross-references with full confounding disclosure live here. HIGH benefit for the analytical reader. NEGATIVE benefit on Tier 1 pages where the stressed reader needs their situation, not a research paper.

**Tier mapping:** Tier 3 (Discover). Analytical content.

**Tier 4 (Distribute):** Distribution assets derived from Tier 3 findings. Charts, summaries, social media formats. One finding, one chart, one sentence, link to depth. Not a separate page type -- a derivative format.

### The DUI Example: Concrete Page Inventory

For Florida DUI under this architecture:

- Tier 1: Florida Statute 316.193 (one page)
- Tier 2 - Charge: DUI in Florida (one page)
- Tier 2 - Situational: First Offense DUI Florida, Second Offense, Felony DUI, DUI with Injury, DUI Refusal (4-8 pages, each only where data supports clean filtering)
- Tier 2 - County: DUI in Miami-Dade, Broward, etc. (5-10 pages, each only where all three conditions met)
- Tier 3: Cross-county variance, temporal trends, etc. (number determined by findings)
- Tier 4: Charts and shareable assets from Tier 3

Total: approximately 12-25 pages. Not 67+. Each earns its existence.

### Charge-to-Statute Mapping Requirement

The mapping from charge name to statute code(s) must be defined per practice area before building the charge page.

Clean mappings: "DUI" → 316.193 (and subsections). "Battery" → 784.03. One statute, clear.

Messy mappings: "Drug Possession" → 893.13 (controlled substances, multiple subsections), 893.147 (paraphernalia), potentially others. Which statutes does "Drug Possession in Florida" include? Different answers produce different statistics.

For each practice area: identify all relevant statute codes, define inclusion/exclusion with reasoning, document in methodology, disclose included statutes in inline evidence. For ambiguous mappings, consider splitting into more specific pages ("Marijuana Possession" vs. "Cocaine Possession") rather than forcing a single "Drug Possession" page. [Data Truthfulness requirement.]

---

## Section 6: County Data as Interactive Layer

### The Principle

County-level data renders as an interactive feature within charge pages and situational pages. The reader selects their county and sees county-specific data in context of the statewide picture.

### How It Serves the Reader

Default view: statewide data as primary display. The BLUF uses statewide statistics. This is the robust, high-N anchor.

Interactive element: county selector allows the reader to view their county's data alongside statewide data. Always in comparison, never in isolation.

"Orange County: 68% conviction rate | Statewide average: 63% | Range across Florida: 45%-82%"

If the county has been trending differently recently: "Orange County's conviction rate increased from 58% in 2021 to 68% in 2025." Genuine, actionable context without being advice.

The comparison IS the value. County data in isolation lacks baseline context. County data in state context helps the reader calibrate expectations.

### Data Threshold Handling in the Interactive Element

For counties with sufficient data: full disposition distribution, comparison to state average, trend if meaningfully different.

For counties with limited data: data displays with sample size prominently stated. "Based on [N] cases from [date range]. This sample size is small and statistics may not reflect typical patterns." Reader gets what exists with honest context. They evaluate reliability.

For counties with no/insufficient data: "Data for [County] is not available in this dataset" or "Fewer than [N] cases available, insufficient for reliable statistics." Transparent, honest, doesn't present unreliable numbers.

### How It Works for the LLM

The complete county-level dataset exists in the page's JSON-LD schema regardless of visible rendering state. The machine reads all county data, always, structured as Dataset with StatisticalVariable entries per county. The LLM doesn't need to interact with a dropdown.

- Human sees: statewide data by default, county data on interaction
- LLM sees: statewide AND all county data in structured format, always
- Statewide statistics: in both visible content and schema
- County-level statistics: in schema always, visible on human interaction

This satisfies the visible/invisible principle: human-facing content governed by Reader Benefit, machine-facing structure governed by Machine Confidence, operating in different layers of the same page.

### Technical Implementation Options [Not Converged]

**Option A: Static HTML with county data present but visually hidden.** All county data in HTML source, displayed on CSS/JS toggle. Simplest for crawlers. Potentially large page source.

**Option B: Server-rendered, county data loaded on interaction.** Base page with statewide. County fetched from API on selection. JSON-LD in page head contains full dataset regardless. Smaller initial load. Requires server infrastructure.

**Option C: Static page, JSON-LD as single source of truth.** JSON-LD comprehensive. Visible HTML shows statewide. Lightweight JavaScript reads from structured data to render county views. Single source of truth drives both machine and human layers.

**Option D: Pre-rendered accordion/expandable elements.** Each county's section pre-rendered in HTML but collapsed by default. User expands. Fully static, fully crawlable. Long page source.

**Progressive enhancement requirement:** Whatever approach is chosen, define the no-JavaScript fallback explicitly. Pre-render all county data in HTML. Use CSS/JS to collapse into interactive element for capable browsers. The page works without JavaScript. JavaScript makes it better.

**JSON-LD as proto-API:** Design the JSON-LD schema with clean field names, consistent structure, and documentation as if it were an API response. When Phase 2+ data products are built (API feeds, licensed datasets, dashboards), the "API" is already written -- it's the JSON-LD extracted from page source.

Resolve during Phase 1A prototyping.

---

## Section 7: Per-Tier Reader Models and Content Inclusion

### The Negative Space Principle

Reader Benefit is not "put helpful information on the page." It is equally "exclude information that doesn't serve this specific reader at this specific tier in their specific cognitive state." The negative space -- what is purposely absent -- is as much a design decision as what is present.

The default instinct (for LLMs and content producers) is comprehensiveness: if data exists and is topically relevant, include it. This instinct must be overridden. Data that is topically relevant but doesn't serve the reader's actual need at this tier is noise. Noise degrades the page for the human even if it enhances it for Machine Confidence. Per the dependency ordering, Reader Benefit wins.

### The Reader-LLM Distinction

Every page has two consumers: the human reader and the LLM. When they diverge -- when something helps the LLM but doesn't help the human -- the implementation is:

Human-facing content governed by Reader Benefit. Machine-facing structure governed by Machine Confidence. Different layers, same page.

The human sees content that serves them. The LLM sees the same content plus schema annotations, JSON-LD, entity relationships in code, and metadata the human never encounters.

**The signal to watch:** If a content decision is justified primarily by "this helps the LLM cite us" rather than "this helps the reader," the data should move to schema, not visible content.

### Tier 1: Statute Page Reader

**Who:** Person just charged or cited. Searched statute code from paperwork. Specific charge, specific jurisdiction.

**Cognitive state:** Acute stress. Fear. Confusion. Urgency. Cognitive bandwidth severely constrained. Scanning for anchors, not reading.

**Device:** Overwhelmingly mobile.

**Scan behavior:** (1) "Is this my charge? My state/county?" → BLUF confirms or they bounce. (2) "What's going to happen to me?" → disposition data, realistic outcomes. (3) "What makes it beatable?" → self-diagnostic questions. (4) Related charges, next steps, contributor. (5) Will NOT read: methodology, temporal trends, demographic breakdowns, full statute text on first visit.

**Natural scan-stop:** After "what makes it beatable." Everything below is second-pass.

**Would bounce on:** Wall of data tables. Stat codes instead of plain English. Leading with max penalties. Performative empathy.

#### Tier 1 Content Inclusion Matrix

| Data Element | Benefit | Reasoning |
|---|---|---|
| BLUF: charge name, county, disposition summary | HIGH | Immediate orientation and outcome answer |
| Disposition distribution for their county | HIGH | Directly answers "what's going to happen to me" |
| Adjudication Withheld explanation | HIGH | 22% of dispositions. Reader must understand this isn't conviction. |
| "What makes it beatable" self-diagnostic questions | HIGH | Empowers case evaluation. Negative space -- no competitor provides this. |
| Related charges via co-occurrence | HIGH | Multi-charge reality. Reader may not know they face additional charges. |
| What to do next / contributor placement | HIGH | Actionable. Natural attorney engagement transition. |
| Charge severity breakdown | MEDIUM | Useful but secondary. Second-pass content. |
| Sentence ranges for convicted cases | MEDIUM | Relevant at "what if convicted" stage. Not first-scan. |
| Full statute text (LegalCode schema) | LOW | Completeness. Most don't read on first visit. Bottom of page. |
| Temporal trends | LOW | Doesn't help act on current charge. Bottom or omit. |
| Statewide comparison | LOW unless outlier | "48% dismissal vs. 5% statewide" = HIGH. "64% vs. 63%" = noise. |
| Methodology (inline brief + linked full) | LOW visible / HIGH linked | One sentence source citation inline. Full methodology linked. |
| Demographic breakdowns | NEGATIVE visible / ELIGIBLE schema-only | Doesn't help this reader's situation. May increase anxiety. This data serves Tier 3 analytical readers. Eligible for inclusion in JSON-LD schema for Machine Confidence without visible rendering. |
| Representation type outcomes | NEGATIVE visible / ELIGIBLE schema-only | May increase anxiety without actionable value. Requires confounding disclosure adding complexity at wrong tier. Serves Tier 3. Eligible for schema-only. |
| Full county data tables (all 56 counties) | NEGATIVE | Researcher content. This reader cares about their county only. |
| Raw data exports | NEGATIVE | Researcher/journalist tool. Not this reader. |

### Tier 2: Charge Page Reader

**Who:** Person searching by charge name ("DUI in Florida"). Pre-charge worried, early-stage charged, comparison-shopping for attorneys, or family member researching.

**Cognitive state:** Elevated concern, lower acute stress than Tier 1. Broader information need. More cognitive bandwidth.

**Device:** Mixed mobile/desktop. More desktop (deliberate research session).

**Scan behavior:** (1) Confirmation ("Is this about DUI in Florida?"). (2) Big picture (penalty tiers, statewide overview). (3) Their situation within the landscape. (4) Reads more linearly than Tier 1. Will scroll multiple sections if well-organized.

**Natural scan-stop:** After penalty tiers and statewide overview. Continues if in deeper research mode.

#### Tier 2 Content Inclusion Matrix

| Data Element | Benefit | Reasoning |
|---|---|---|
| BLUF: charge overview, statewide disposition | HIGH | Orientation and immediate answer |
| Penalty tiers (first offense through felony) | HIGH | Core need: "what am I facing?" |
| AW explanation | HIGH | Essential Florida context |
| Statewide disposition overview | HIGH | The big picture they came for |
| Cross-county variance summary (range, not full table) | HIGH | "Dismissal rates range X% to Y%" is a finding, not 56 rows |
| Charge co-occurrence patterns | HIGH | "If charged with DUI, often also charged with..." |
| Procedural timeline | HIGH | Planning ahead. Arrest through resolution. |
| Links to Tier 1 county pages | HIGH | Drill into specific county. Navigation, not duplication. |
| Contributor section | HIGH | Closer to attorney engagement than Tier 1. |
| Severity breakdown | MEDIUM | Useful context, secondary |
| Defense angles (generalized) | MEDIUM | Less specific than Tier 1 but still useful |
| Representation type with confounding caveat | MEDIUM | Relevant for attorney comparison-shopping |
| Sentence aggregates | MEDIUM | Sets expectations |
| Temporal trends (brief) | LOW | "Outcomes shifted X% since 2019" sufficient |
| Full 56-county table | LOW to NEGATIVE | The finding (range) serves. Full table is researcher content. Bottom appendix if included. |
| Demographic breakdowns | NEUTRAL to LOW | Not primary need. Secondary section if included. |

### Tier 3: Synthesis Page Reader

**Who:** Categorically different reader. Journalist, attorney analyzing patterns, policy researcher, academic, reform advocate, LLM extracting analytical data.

**Cognitive state:** Analytical. Not under personal stress. Full cognitive bandwidth. Reading to evaluate, not cope. Will scrutinize methodology. Will check sample sizes. Cite/don't-cite decision based on observed rigor.

**Device:** Desktop/tablet. Research session.

**Scan behavior:** (1) The finding (BLUF). (2) "Interesting enough?" If trivial, bounce. (3) Primary visualization -- does chart clearly show claimed pattern? (4) Supporting analysis (reads linearly). (5) Methodology (reads carefully -- sample sizes, normalization, confounders, sources). (6) Download data/methodology if available. (7) Cite/don't-cite decision.

**Would bounce on:** Finding buried under background. No clear BLUF. No methodology. No sample sizes. Unclear visualizations. Editorializing.

#### Tier 3 Content Inclusion Matrix

| Data Element | Benefit | Reasoning |
|---|---|---|
| BLUF: the finding | HIGH | Here for the finding. Front-load. |
| Primary visualization (one chart, one finding) | HIGH | Visual evidence the finding is real |
| Full supporting data table | HIGH | Wants complete data, not summary |
| Methodology (inline, detailed) | HIGH | Evaluates citability based on rigor |
| Sample sizes per data point | HIGH | Non-negotiable |
| Confounding variable disclosures | HIGH | Non-negotiable. Absence = not citable. |
| Source citations (dataset, date, URL) | HIGH | Provenance chain. May verify independently. |
| Demographic cross-references with disclosure | HIGH | This is where this data belongs. Analytical intent matches analytical content. |
| Representation type with full confounding | HIGH | Same. Analytical context. |
| Temporal trends (detailed) | HIGH | Trend data is a primary finding type |
| Downloadable data/methodology | MEDIUM to HIGH | Researcher expectation |
| Contributor section (if expert commentary) | NEGATIVE if ad-style / NEUTRAL-MEDIUM if attributed expert Tier C analysis | "Attorney advertisement" undermines neutrality. "Practicing attorney explains why this county's rate is what it is" enriches analysis. Format determines benefit level. |
| Basic charge explanations | NEGATIVE | This reader knows what DUI is |
| Penalty tables | NEGATIVE | Not facing charges |
| "What to do next" / procedural guidance | NEGATIVE | Not charged |

### Tier 4: Distribution Asset Reader

**Who:** Social media consumer, journalist receiving a pitch, editor evaluating coverage, LLM scanning for notable data.

**Cognitive state:** Attention-scarce. Scrolling. ~3 seconds to demonstrate engagement value.

**Content principle:** One finding. One chart. One sentence. Link to depth. Everything else is negative space for this tier.

### The Editorial Filtering Principle

Data exists in the pipeline once. Normalized, cross-referenced, validated once. Where it renders as visible content: per-tier Reader Benefit decision. Where it renders as invisible structure (schema, JSON-LD): Machine Confidence decision. These are independent.

A data element can simultaneously: render visibly on Tier 3 (Reader Benefit for analytical reader), render as schema-only on Tier 1 (Machine Confidence without visible noise), not render at all on Tier 4 (neither served).

Page templates are defined by: Who is the reader? What cognitive state? What do they benefit from seeing? What do they NOT benefit from seeing? What scan path? Where is the scan-stop? What would make them bounce? Data availability determines what CAN populate. Reader Benefit determines what DOES populate.

---

## Section 8: Information Sequencing

### The Sequence and Its Reasoning

Every position is derived from Jobs-to-be-Done analysis, not from style preference or convention.

**Position 1: "What this charge means."** Plain language, 1-2 sentences. BLUF. Immediate orientation. "You have been charged with X. Here is what that means." Every legal site does this, but most bury it under firm marketing or emotional language. The organic constraint: the reader needs to know what they're dealing with, immediately.

**Position 2: "What typically happens."** The emotional relief point. The reader's anxiety is about realistic outcomes -- "am I going to prison?" -- not statutory maximums. Every other legal site leads with maximum penalties because it's dramatic and scares people into calling. That's a conversion tactic, not a helpfulness tactic. The organic constraint: the reader's primary emotional need is realistic exposure. County-level disposition data (63% conviction, 22% AW, 7% diversion, 5% dismissed) provides that. It replaces fear with information. This is where Tier B data does the most direct emotional work.

**Position 3: "What makes it beatable."** Once acute anxiety is partially addressed, the reader is cognitively ready to evaluate their situation. Self-diagnostic questions ("Was the traffic stop legal? Was the breathalyzer calibrated? Were you read your rights?") help assess whether their case has weaknesses. This is the "Negative Space" positioning -- the thing no other legal content provides because it requires genuine legal knowledge, not statutory recitation.

**Position 4: "Related charges."** Multi-charge reality. DUI often comes with open container, driving on suspended, reckless driving. Charge co-occurrence data (from UNIQUE_CORRELATION_ID grouping) addresses this. No other site maps this.

**Position 5: "What to do next."** Procedural guidance. This is where the contributor placement naturally sits -- the attorney is the expert who navigates the specific process. The placement is contextually earned.

**Position 6: "Full legal detail last."** Statute text, penalty table, elements of the offense. Important for completeness. Not what the reader needs first. Every other site leads with this because it's the easiest to produce. Leading with it is a synthetic constraint born from production convenience.

### Intent Inversion as Recurring Calibration Tool

"What would guarantee absolute failure?" reveals that standard industry practices are often close to the failure state. Leading with max penalties = guaranteed anxiety escalation. Performative empathy = guaranteed trust erosion. Generic language = guaranteed irrelevance.

The "What to Avoid" list (performative empathy, max penalties, generic language, overpromising, conflating charges) is inversion-derived. It should be re-derived for each new page type, charge type, and jurisdiction. The failure modes differ. Run the inversion when entering new territory. Log results alongside the editorial decision register.

---

## Section 9: The Data Pipeline (Data Journalism Reframe)

This project's pipeline is a data journalism pipeline, not an SEO content pipeline. The workflow, rigor standards, and credibility architecture map to data journalism (Our World in Data, ProPublica) rather than content production.

### The Six-Stage Pipeline

**Stage 1: Procurement.** Get the data. CJDT Clerk data, SAO data, secondary sources. Mechanical. No judgment. Whether data arrives as bulk CSV, FOIA response, commercial API export, or formal request result, once it enters the database the same pipeline applies. The acquisition method varies by jurisdiction; everything downstream is identical.

**Stage 2: Harmonization.** Two distinct operations:

*Normalization within a single dataset:* Standardizing terms (mapping "nolle prosequi" to "dismissed"), handling formatting variance between counties, resolving ambiguous codes. The Normalization Authority Protocol: legal SME review per state, published mapping tables, unmappable designations permitted. Florida-specific challenges: AW as distinct category, "Dismissed" not distinguishing prosecutorial/judicial, statute formatting variance, Broward COUNSEL_CATEGORY 100% missing.

*Harmonization across datasets:* Aligning two different systems that weren't designed to communicate. Cross-referencing CJDT disposition data with DHSMV administrative suspension data. The linkage test: is there a common identifier (case number, PERSON_ID, citation number, county + date matching)? If no common identifier, cross-reference is aggregate-only (total arrests vs. total dispositions per county per year), not case-level. Knowing which level of linkage is possible is the first credibility gate. Don't assume linkage works. Test it.

**Stage 3: EDA (Exploratory Data Analysis).** The credibility protection mechanism. Before publishing anything, run every cross-reference privately. Do the numbers make sense? If dispositions exceed arrests for a county, something is wrong with the linkage. If BAC cross-referenced with outcomes shows no correlation, either the linkage is broken or the finding is genuinely null (publishable if methodologically sound). This stage catches the "one wrong move" before it becomes public.

Every cross-reference is tested internally before any finding reaches a public page. The editorial decision register logs not just published findings but tested cross-references that failed or were killed. A killed cross-reference documented in the register is evidence of rigor.

**Stage 4: Editorial Triage.** The publish/kill decision. Three conditions, all required:
1. **Intent exists** -- a real audience needs this
2. **Data says something** -- meaningful variance, outliers, counterintuitive findings
3. **Comparison is structurally valid** -- apples to apples, confounders acknowledged

Dead Man's Zone avoidance: generic comparisons confirming expected patterns are killed here.

*Editorial Decision Register (formal schema):* Proposed analysis → data result → publish/kill decision → reasoning → threshold applied → confidence level. First-class project artifact. Over time becomes training data for the automated novelty detection gate. Encodes editorial judgment -- the thing hardest for a competitor to replicate.

*Day-one auto-kill rules (pre-filters):*
- Variance spread below defined threshold → auto-kill (calibrate from Phase 1A data)
- Total sample below defined N → auto-kill
- Finding already fully represented at another aggregation level → auto-kill (internal redundancy)

*Novelty detection options (convergence path):*
- Phase 1: Option E (human-in-the-loop, all decisions logged)
- Target: Option D (multi-signal composite trained on logged decisions)
- Components: Options A (statistical deviation) and B (minimum variance range) as automated pre-filters

**Stage 5: Documentation.** Methodology transparency following the Our World in Data model. Exhaustive provenance documentation. The finding is the headline. The methodology is the credibility.

*Claim-evidence architecture:* Every statistical claim within a content block includes within that block: source name, date range, sample size, critical caveats. Full methodology linked. Each block self-sufficient for verification. An LLM extracting one block gets the claim and enough evidence to assess confidence.

*RAG-optimized semantic chunking:* Content structured into 200-400 word self-contained blocks. Each independently retrievable without surrounding context. Reader Benefit determines block boundaries (a section needing 500 words for complex data gets 500 words). The range is a calibration target, not a rigid rule.

*Confounding variable disclosure:* Any cross-reference involving demographic or representation-type variables includes explicit methodology disclosure of uncontrolled variables (pre-trial detention, charge severity, prior record, indigency). Report numbers. State limitations. Don't imply causation.

**Stage 6: Publication.** Visual encoding (Tufte-informed: one chart, one finding, maximize data-ink ratio, minimize chartjunk). Schema annotation. Pillar framework governs all rendering decisions.

*Visualization as structural strategy (not cosmetic):* Charts and data visualizations are a primary differentiation mechanism, most critical at Tier 3 where visual presentation of cross-county variance IS the content. Visualizations must be both human-readable (clean, clear, immediately comprehensible) and machine-readable (underlying data accessible via schema annotation or structured data block). LLM-readable chart annotation: technical approach to be resolved during Phase 1A (SVG with structured attributes vs. accompanying JSON-LD vs. accessible data table vs. combination).

*Dimensionality reduction principle:* One chart. One variable's variation. One finding. Sorted for clarity. Supporting data table available separately. Schema annotation on the chart's underlying data. Different tiers benefit differently: Tier 2 gets a summary chart, Tier 3 gets the chart plus full table, Tier 4 gets the chart as the shareable asset.

### Maintenance and Refresh

*Silent normalization corruption detection:* After each data refresh, compare refreshed statistics against prior period. If any metric changes more than defined threshold, flag for human review before propagation.

*Cascade refresh rule:* Any data refresh updating a Tier 1 page must cascade to Tier 2 charge page(s) aggregating that data, any Tier 3 synthesis page referencing it, and any Tier 4 asset derived from affected findings. Refreshes are atomic per update event: all affected tiers update together or none do. Partial propagation creates cross-tier contradictions that degrade domain trust.

*Refresh cadence (preliminary, calibrate Phase 1):* Statute text annually after legislative sessions. Disposition statistics annually or semi-annually for high-volume charges. Low-volume jurisdictions flagged with "small sample" notices. Temporal trend pages on same cadence as underlying data. Contributor content verified quarterly.

*Refresh cost scaling:* Each new jurisdiction increases maintenance burden. Cost scales linearly while marginal value per jurisdiction scales sub-linearly. Crossover point exists. Model post-Phase 1.

### Agentic Workflow Architecture

First jurisdiction manual. Edge cases discovered during manual processing make the agentic pipeline correct.

Authority Ladder governance: Rung 1 (agent proposes, human decides) for initial page generation and contributor content. Rung 3 (agent stages, human authorizes) for validated batch generation. Rung 4 (agent acts within constraints) for data refresh with materiality triggers for review.

### Phase 1 Scope: Four Required Outputs

1. **Synthesized statistics** -- validating or killing the core thesis
2. **Structural compatibility map** -- which cross-references are buildable, which need caveats, which are impossible
3. **Editorial decision register** -- logged judgments as calibration data
4. **Cost and timeline profile** -- actual costs, actual time, actual refresh burden

---

## Section 10: Schema and Machine-Readability Strategy

### "Make It Stupidly Obvious for Machines"

Structure everything so LLMs and search engines can unambiguously identify what the data represents, where it came from, and why they should trust it. Not an SEO tactic. The core product philosophy. The data's value is zero if machines can't parse, verify, and confidently cite it.

### Schema Gap [CONFIRMED]

Source code inspection of seven sites:

| Schema Type | Justia | FindLaw | Nolo | Shouse | Avvo | MFJ | CourtListener | FCF |
|---|---|---|---|---|---|---|---|---|
| Dataset | No | No | No | No | No | No | No | **Yes** |
| StatisticalVariable | No | No | No | No | No | No | No | No |
| FAQPage | No | No | No | No | No | Partial | No | **Yes** |
| Article | No | **Yes** | **Yes** | No | No | No | No | Yes |
| LegalCode | No | No | No | No | No | No | No | No |
| Person (credentials) | No | **Yes** | **Yes** | No | No | No | No | No |
| reviewedBy + hasCredential | No | **Yes** | No | No | No | No | No | No |
| ClaimReview | No | No | No | No | No | No | No | No |

### Schema Is Infrastructure, Not Moat

FCF has perfect Dataset + FAQPage schema, ranks #1 organically, and is cited in ZERO AI Overviews. [CONFIRMED] Schema alone does not generate citation. AI citation requires schema + domain authority + E-E-A-T, built incrementally over time. Schema is the necessary infrastructure making other layers machine-readable. The moat is what's inside the schema.

### Schema Implementation Priority

1. **FAQPage** -- highest proven citation lift, translates data into Q&A pairs. Table stakes (FCF uses it).
2. **Article + Person + hasCredential/reviewedBy** -- FindLaw E-E-A-T benchmark. Connection points built but empty at launch. Person entities added when contributors join (Phase 2+).
3. **Dataset with variableMeasured** -- FCF uses it. Table stakes for data pages. Design as proto-API (clean field names, consistent structure).
4. **ClaimReview** -- wraps key statistical claims with links to source data and verification. Signals machine trust. Apply to primary findings per page (BLUF statistic, headline cross-reference). Not every claim -- calibrate density during Phase 1A to avoid schema bloat.
5. **LegalCode** -- zero competitors including FCF. Unique for statute text pages.
6. **dateModified** -- freshness signal. Trivial to implement. Each refresh updates it.
7. **BreadcrumbList with @id** -- navigation context.
8. **StatisticalVariable** -- experimental Google support but unique.
9. **DefinedTerm / DefinedTermSet** -- legal terminology. Only FindLaw uses this.
10. **LegislationObject** -- statute metadata. Future-proofing.
11. **DataCatalog / DataDownload** -- Phase 2+ when downloadable assets ship.

### @id Interconnection Strategy

Schema types interconnected via @id to form a page-level knowledge graph, not isolated fragments.

**At launch (Phase 1):**
- Site-level Organization entity with @id
- Each Dataset references Organization as creator via @id
- Each Article references Organization as author via @id
- StatisticalVariable instances reference parent Dataset via @id
- BreadcrumbList connects pages via @id

**At Phase 2+ (contributors join):**
- Person entities with hasCredential connect to Article via reviewedBy
- Person connects to Organization via memberOf
- Existing @id chain extends without rebuilding

Extensibility: the @id graph must accommodate Person entities being added later without restructuring. Design connection points now even though Person nodes are empty at launch.

### Schema Validation Requirement

All prototype pages must pass Google's Rich Results Test and Schema.org validator during Phase 1A. If schema throws errors, the distribution mechanism is broken before Phase 1B.

**Schema density concern:** A charge page with statewide stats + 56 counties in JSON-LD + FAQPage + Article + ClaimReview could produce a very large JSON-LD block. Fallback hierarchy if validation fails: (a) statewide Dataset + FAQPage first (proven citation drivers), (b) county data in separate linked Dataset referenced by @id, (c) ClaimReview limited to top 2-3 findings per page.

### Partial Extractability

The project benefits from AI citation (authority) while the contributor model benefits from click-through. The depth driving click-through is natural. An AI Overview extracts the BLUF headline. It cannot extract the full disposition distribution, the co-occurrence table, the temporal trend, the severity breakdown, the representation-type cross-reference, or the contributor's contextual analysis. The statistics are the hook. The full analytical picture is the product. Not anti-extraction design -- genuinely richer content than a snippet captures.

### Site-Level E-E-A-T

No named attorney required at launch. Schema connection points built but empty. Phase 2+. [FIRM DECISION]

Site-level credibility from: methodology transparency (published normalization rules, source documentation), About page (named individuals, clear mission), data quality itself (accurate, well-sourced, properly caveated). The methodology is the credibility.
## Section 11: Multi-Source Data Framework

### The Multiplicative Logic

One dataset (CJDT) gives you statistics. FCF already does this. Two cross-referenced datasets give you findings. Three or more give you findings that literally cannot exist anywhere else because nobody has connected the sources. This is where the real information gain lives.

Each additional source doesn't add linearly -- it multiplies. Each new source can be cross-referenced with every existing source. The number of possible cross-references grows combinatorially while the credibility protection pipeline (Stage 2-4: harmonization → EDA → editorial triage) ensures only valid combinations reach publication.

### The Case Lifecycle and Data Sources

The full lifecycle of a criminal case:

**Incident → Arrest → Filing Decision → Arraignment → Disposition → Sentencing → Post-Conviction**

CJDT covers roughly Filing-through-Sentencing. Every stage outside that window is a different data source. Every connection between stages is a cross-reference producing net-new findings.

### Source Inventory for Florida

**Source 1: FDLE SAO (State Attorney) Case Reports.** [CONFIRMED portal exists; UNVERIFIED field contents]

Same FDLE CJDT portal, same statutory mandate (F.S. 900.05), same download mechanism. Likely adds: prosecutor filing decisions, case routing (felony vs. misdemeanor filing), pre-court diversion referrals.

Cross-reference with Clerk data: the prosecution funnel. "Of all cases referred for DUI prosecution, X% resulted in formal charges." Nobody publishes this.

Potential headlines: "One in four DUI arrests in [County] never results in formal charges." County-level variance in prosecutorial filing rates is extremely newsworthy.

Obtainability: HIGH. Investigation priority: Phase 1A week 1.

**Source 2: Florida DHSMV (Highway Safety and Motor Vehicles).** [UNVERIFIED]

DUI has dual tracks: criminal (court, CJDT) and administrative (license suspension, DHSMV). Likely contains: license suspension/revocation data, hardship license applications, DUI school enrollment, ignition interlock installations, implied consent refusal records, potentially BAC levels.

Cross-reference with CJDT: "Of defendants acquitted or dismissed, X% still had license suspended through administrative process." BAC-to-outcome correlation: "DUI defendants with BAC over 0.15 convicted at X% versus Y% near 0.08 threshold." BAC-to-outcome is one of the most searched-for DUI data points and it literally doesn't exist in published structured form anywhere.

Potential headlines: "Your license suspension starts before your trial -- X% lose driving privileges within 10 days of arrest regardless of criminal outcome." "BAC above 0.15 doubles conviction rate."

Obtainability: MODERATE to UNKNOWN. May require FOIA. Investigation priority: Phase 1A-1B parallel track.

**Source 3: FDLE Arrest / UCR Data.** [UNVERIFIED]

FDLE publishes arrest data through Uniform Crime Reports. Likely contains: arrest counts by county, offense type, demographics, time period.

Cross-reference with CJDT: the arrest-to-disposition funnel. "X DUI arrests in Florida in 2024. Y% resulted in charges. Z% of charged were convicted." The complete criminal justice funnel. Nobody publishes this because it requires connecting three systems.

Potential headline: "From arrest to conviction: only X% of Florida DUI arrests result in a guilty finding."

Obtainability: MODERATE. Linking challenge: connecting arrest record to CJDT disposition requires common identifier. Investigation priority: Phase 1B.

**Source 4: Florida DOC (Department of Corrections).** [UNVERIFIED]

Likely contains: inmate records, admission/release dates, time served vs. sentenced, facility data, post-release supervision.

Cross-reference with CJDT: post-conviction picture. "DUI defendants sentenced to 12 months serve average of X months."

Obtainability: MODERATE. Linking challenge same as arrest data. Investigation priority: Phase 2.

**Source 5: FLHSMV Crash Data.** [UNVERIFIED]

DUI-involved crash reports. Injury severity, fatality data, location.

Cross-reference with CJDT: "Of DUI crashes with serious injury, X% result in felony charges, Y% in conviction."

Obtainability: MODERATE. Investigation priority: Phase 2.

**Source 6: County Jail Booking Data.** [UNVERIFIED]

Some counties publish booking/intake data. Would add: pretrial detention status, bail amounts.

Cross-reference with CJDT: controls for the key confounding variable in representation-type analysis. "DUI defendants held pretrial X times more likely to plead guilty regardless of attorney type."

Obtainability: LOW-MODERATE (fragmented by county). Investigation priority: Phase 2.

### Credibility Protection for Multi-Source Work

The harmonization stage (Pipeline Stage 2) catches mismatches before they reach publication. The EDA stage (Stage 3) validates every cross-reference privately. The editorial triage stage (Stage 4) kills findings that don't survive scrutiny.

Specific protections: if datasets lack a common identifier, cross-reference is aggregate-only (honest about granularity). If linkage produces impossible numbers (dispositions > arrests), linkage is broken and cross-reference is killed. If harmonization requires assumptions that could distort findings, assumptions are disclosed or the cross-reference is not built.

The editorial decision register logs every cross-reference attempt including failures. Documentation of what was attempted and why it was killed is evidence of rigor.

### Reference Models

**Our World in Data (Max Roser):** Gold standard. Chaotic global datasets from hundreds of uncoordinated sources, harmonized, presented with exhaustive methodological transparency.

**ProPublica:** Building interactive databases from fragmented public records. Experts at knowing which synthesized data points matter.

**Bellingcat:** OSINT pioneers synthesizing seemingly unrelated data points into irrefutable evidence.

**Edward Tufte:** Foundational principles of data visualization with integrity and efficiency.

**Nate Silver / FiveThirtyEight (historical):** Aggregating localized, differently weighted data into probabilistically sound visualizations.

---

## Section 12: Data Landscape

### Florida CJDT: The Confirmed Foundation

[CONFIRMED via direct download and inspection of 4,092,482 records across 55 columns.]

**Source:** FDLE Criminal Justice Data Transparency Clerk Case dataset. Azure Blob Storage direct download. No login, no rate limits. 207 MB compressed, 1.84 GB uncompressed. Mandated by F.S. 900.05.

**High-confidence fields (0% or near-0% missing):** Disposition, STATUTE, FCIC_Category, Level, Degree, Race, Ethnicity, Sex, Age, Indigent, COUNTY_DESCRIPTION, JUDICIAL_CIRCUIT, UNIQUE_CORRELATION_ID, PERSON_ID, DISPOSITION_DATE.

**Moderately usable:** COUNSEL_CATEGORY (~13% missing, 100% missing Broward), SENTENCING_DATE (~15-24%), COURT_COST (~36%), SENTENCE_CONFINEMENT (~66%, expected for non-confinement), PROBATION_DURATION_DAYS and MAXIMUM_TERM_DURATION_DAYS (populated for sentenced cases).

**Not usable:** FINE/RESTITUTION (77-78% missing), PROSECUTOR_FILING/SENTENCE_STATUS/habitual offender flags (100% empty), US_CITIZENSHIP (78% "Not Available").

**DUI subset:** ~340,000-350,000 records. Filter: FCIC_Category = "DUI-Unlawful Blood Alcohol" (cleanest) or STATUTE LIKE '316.193%' excluding 316.1935 and 316.1939.

**Disposition categories [CONFIRMED]:** Adjudicated Guilty (~63%), Adjudication Withheld (~22%), Pre-Trial Diversion (~7%), Dismissed (~5%), plus ~11 rare categories. 0% missing.

**Case linkage:** One row per charge. UNIQUE_CORRELATION_ID links charges in same case. Average 1.14 charges per case, max 23.

**County coverage:** 56 confirmed of 67. Missing: Brevard (~600K), Charlotte (~200K), Okaloosa (~200K), Sarasota (~450K). ~1.4M residents' counties unrepresented. Coverage gap to be quantified in Phase 1A.

**Critical corrections:** No judge identifier (only Judicial Circuit). Not all 67 counties. Financial data unusable. Shouse is 86K not 3.1M.

**SAO dataset:** FDLE also publishes State Attorney Case Reports. May contain prosecutor filing decisions. Flagged as Phase 1A investigation item.

**Florida law change:** Trenton's Law (HB 687, effective October 1, 2025) changed DUI penalties for repeat offenders and breath test refusal. All Florida DUI content must reflect.

### Buildable Cross-References from CJDT

| Cross-Reference | Fields | Feasibility | Caveats |
|---|---|---|---|
| Disposition × County | Disposition, COUNTY | HIGH | 56 of 67 counties |
| Disposition × Representation | Disposition, COUNSEL_CATEGORY | MODERATE | County-dependent; Broward excluded |
| Disposition × Demographics | Disposition, Race/Sex/Age | HIGH | Confounding disclosure required |
| Disposition × Indigency | Disposition, Indigent | MODERATE | "Not Available" dilutes |
| Disposition × Severity | Disposition, Level/Degree | HIGH | Clean |
| Charge Co-occurrence | UNIQUE_CORRELATION_ID, STATUTE | HIGH | Case-level grouping |
| Temporal Trends | DISPOSITION_DATE, Disposition | HIGH | 2018-2026 |
| Sentence Distributions | CONFINEMENT, PROBATION, TERM | MODERATE | Convicted cases only |
| Rural vs. Metro Cohort | COUNTY (grouped) | HIGH conceptually | Requires classification |
| First vs. Repeat | PERSON_ID | MODERATE | 2018+ window only; validate PERSON_ID reliability first |
| MFJ Historical Baseline | MFJ data (2013-2017) × CJDT | HIGH for FL | Neither source produces temporal findings alone |

### PERSON_ID Reliability [Phase 1A Blocker]

The first-offense filter, repeat-offender analysis, and several cross-references depend on PERSON_ID correctly linking individuals across charges and counties over time. If the field has data quality issues (different IDs for same person across counties, IDs that reset), every analysis relying on individual tracking is compromised.

Validation during Phase 1A week 1: cross-check within cases (same UNIQUE_CORRELATION_ID should have same PERSON_ID), cross-check across cases (patterns suggesting fragmentation or over-merging), cross-check across counties where possible. If unreliable, "first offense" pages need different methodology or cannot be built as designed.

### 50-State Landscape [Mixed evidence levels]

3 HIGH: Florida (confirmed), California (reported -- DOJ OpenJustice Portal, needs inspection), Virginia (confirmed but private hobby site, fragile).

16 MODERATE: Arizona, Arkansas, Connecticut, Indiana, Maryland, Massachusetts, Minnesota, New Jersey, New York, North Carolina, North Dakota, South Carolina, Texas, Utah, Washington, Wisconsin.

31 LOW.

Underlying data exists in nearly all states (confirmed by UniCourt/Trellis coverage). Barrier is access model, not data non-existence.

DUI-specific sources beyond court systems: California DMV dashboards, Ohio Breath Instrument Data Center (free bulk), North Carolina Sentencing Commission DWI reports (BAC data), South Carolina SCCPC annual DUI Disposition Reports.

CJARS (University of Michigan / Census Bureau): 40+ states case-level data. Researcher access only. Proves data exists.

The 50-state transparency audit: no existing publication provides a state-by-state assessment of bulk criminal court outcome data extractability. Potentially net-new and publishable as Tier 3/4 asset.

---

## Section 13: Competitive Landscape

### The Structural Hole [CONFIRMED]

No entity publishes consumer-facing, current, normalized, county-level disposition statistics with synthesis, editorial quality, and expert attribution. FCF publishes data without synthesis or editorial quality. MFJ publishes stale synthesis without search visibility. Everyone else publishes explanatory content without data.

### Traffic Landscape [REPORTED, SimilarWeb February 2026]

| Site | Monthly Visits | YoY | Search % |
|---|---|---|---|
| Justia | 5,506,010 | +11.4% | 70.7% |
| FindLaw | 1,632,373 | -11.0% | 68.3% |
| Avvo | 1,100,252 | -25.7% | 65.9% |
| Nolo | 395,349 | -42.3% | 57.2% |
| Shouse | 85,594 | -51.0% | 65.6% |
| MFJ | 1,678 | -41.5% | 24.3% |

The bifurcation: primary source (Justia) grows. Explanatory (Shouse, Nolo) declines 25-51%. AI Overviews cite primary sources and summarize away secondary.

### MFJ Summary

501(c)(3) nonprofit, founded 2011. Strong institutional E-E-A-T (MacArthur, Arnold, Chan Zuckerberg funding; DOJ partnerships). Data last updated January 2022. 20 of 50 states. React SPA -- invisible to crawlers. Zero schema on data pages. ~1,678 visits/month. Downloadable data suitable as historical baseline (2013-2017 cohorts). Validates that data synthesis is valuable enough for millions in investment. Technical failure proves data means nothing without machine-readable structure. [CONFIRMED]

### FCF Summary [CONFIRMED]

Launched March 8, 2026. CourtFile LLC. 4,502 pages. 67 counties × 36 charge types. Lead-generation. Best-in-class Dataset + FAQPage schema. #1 organic rankings for long-tail. ZERO AI Overview citations. No synthesis, no editorial depth, no named experts, no Tier C, zero backlinks.

**What FCF proves:** Schema is necessary but not sufficient. AI citation requires schema + authority + E-E-A-T. FCF has schema without authority or E-E-A-T: zero citations. Google's AI Overview literally says conviction rates are "not readily available" while FCF's page showing the exact answer sits at #1 organically. [CONFIRMED]

**Net-new thesis revision:** Basic CJDT statistics are no longer net-new. Net-new comes from: synthesis (cross-county variance, cohort analysis, temporal trends), editorial quality (information sequencing, contextual explanation, diagnostic framing), multi-source cross-references, Tier C contributor content, and cross-jurisdictional expansion.

### Search Volume [REPORTED + INFERRED]

Total addressable Florida query universe: ~26,500-62,000 monthly searches. County-level data queries: 930-3,340 (low volume, zero competition). Question-format queries: 4,880-12,240 (40-58% AI Overview trigger rate). Charge queries: 6,000-14,800.

AI Overview trigger rates: question queries 46-58%, informational legal 23-78%, county/local data 7-20%. [REPORTED from Ahrefs/SE Ranking studies]

---

## Section 14: Temporal Windowing Strategy

### The Problem

Every published statistic is a function of time. The CJDT data spans ~2018 to present. The choice determines what number appears everywhere, how data ages, and how it compares to external sources.

### Per-Tier Resolution

**Tier 1/2 readers (stressed, current situation):** Trailing multi-year window. These readers need current patterns. A county that shifted from 80% conviction in 2019 to 45% in 2025 is poorly served by a 63% all-time average.

Window length considerations: 1-year (highly current, noisy for low-volume), 2-year (balanced), 3-year (stable but may obscure post-legislative-change shifts like Trenton's Law). The optimal window may differ by charge volume. [Not converged -- calibrate Phase 1A from actual variance patterns.]

**Tier 3 readers (analytical, trends):** Full historical range. Year-by-year or period-by-period breakdowns. The trend IS the finding. The trailing window from Tier 1/2 is contextualized: "Current rate is X%, representing a [direction] from Y% in [earlier period]."

### Display Format

Every statistic includes its window explicitly. Non-optional (Data Truthfulness + Machine Confidence requirement):

"Based on [N] cases from [start year]-[end year], [source]."

Example: "Based on 12,847 DUI cases from 2023-2025, FDLE Criminal Justice Data Transparency dataset."

### Legislative Transition Handling

Trenton's Law (October 2025) changed Florida DUI law. A trailing window including pre- and post-change data mixes two legal regimes. Required disclosure: "Florida DUI law changed effective October 1, 2025. Statistics from before this date reflect prior framework. Post-change data accumulating."

Consider offering post-change-only view when sufficient volume exists, even if trailing window is broader.

### MFJ Historical Baseline

MFJ provides Florida county-level disposition data with 2013-2017 cohorts. Cross-referencing MFJ historical with CJDT current produces temporal findings neither source provides alone. This cross-reference works regardless of the trailing window chosen for primary display.

### Temporal Scope Mismatch for Situational Filtering

Trailing window determines statistics display. But first-offense filter requires looking BACK across full dataset for PERSON_ID history. Two operations: (1) identify population using full dataset, (2) compute statistics on trailing window subset only. Required methodology: "First offense defined as no prior DUI charge for same individual in CJDT (2018-present). Prior history before 2018 not available."

---

## Section 15: Minimum Viable Data Threshold Framework

### Statewide Statistics

Almost always sufficient. DUI statewide: 340K+ records. Even situational subsets: tens of thousands. The threshold question rarely applies at state level. If a charge type has so few cases statewide that statistics are unstable, the charge page may not be warranted (Dead Man's Zone gate).

### County-Level Interactive Element

This is where threshold matters most. Three-tier handling:

**Option A (Hard floor):** Below N, no statistics computed. "Insufficient data for reliable statistics. [N] cases available."

**Option B (Soft floor):** Below threshold, statistics displayed with prominent caveat and exact N. "Based on [N] cases. Small sample -- may not reflect typical patterns."

**Option C (Tiered display, recommended):** Above high threshold: full display. Between thresholds: display with caveat. Below low threshold: no display, only N stated.

Option C gives Reader Benefit maximum information while maintaining Data Truthfulness.

Calibration: compute rates at various sample sizes during Phase 1A, observe volatility. The threshold is where adding/removing a small number of cases meaningfully changes rates. [Not converged on specific numbers.]

### Synthesis Pages

Higher threshold than interactive element. Low-N counties excluded from cross-county comparisons to prevent outlier distortion. Methodology note: "X counties excluded due to samples below [N]."

### County Pages (Conditional)

Highest threshold. Three conditions all required (Section 5). Data volume condition must be meaningfully higher than interactive element threshold.

---

## Section 16: Monetization Architecture

### Phase 1: Contributor Placements

Attorneys pay for contextually relevant editorial placement on pages matching their practice area and jurisdiction. Minimum substantive contribution providing genuine Tier C data (procedural logistics, typical timelines, courtroom context). Generic boilerplate rejected. Quality gate is load-bearing.

**Contributor value in zero-click:** Canonical source association. Each click represents someone demonstrably serious (self-selected through high-intent filtering). Association with the cited source page has value independent of click volume.

**Cold-start constraint:** 6-12 months estimated zero-revenue period. [UNVERIFIED] Recruitment only after pages rank and traffic is demonstrable. Schema connection points built and ready for when contributors join.

### Phase 2+: Potential Additional Interfaces [UNVERIFIED]

Data licensing (API feeds), institutional subscriptions, attorney analytics dashboards, white-label licensing, insurance/risk modeling data. All contingent on dataset scale and ToS compliance. The JSON-LD proto-API approach means the data product is being built inside Phase 1 pages.

---

## Section 17: The Moat Thesis

The competitive moat is the combination of layers individually approachable but collectively expensive and time-consuming to assemble:

1. **Synthesis capability (Tier 3)** -- editorial judgment about what data reveals. FCF doesn't have this. The editorial decision register encodes this judgment over time.

2. **Multi-source cross-referencing** -- findings from combining datasets nobody else has connected. The more sources, the wider the moat. Each additional source multiplies possible findings.

3. **Editorial quality** -- information sequencing, JTBD mapping, diagnostic framing, contextual explanation. The difference between a data table and a resource that helps someone at 2 AM.

4. **E-E-A-T infrastructure** -- named contributors (Phase 2+), methodology documentation, published normalization rules. Required for AI citation alongside schema.

5. **Schema implementation** -- the machine-readability layer. Table stakes given FCF's implementation, but the combination of data schema + E-E-A-T schema + legal schema (LegalCode) + ClaimReview exceeds all competitors.

6. **Tier C contributor network** -- practitioner knowledge that can't be programmatically replicated.

7. **Citation momentum and historical depth** -- temporal advantage that compounds. Historical data enables trend analysis a new entrant can't replicate.

8. **Tier 4 authority building** -- distribution strategy accelerating sandbox exit and building domain authority FCF hasn't pursued.

Schema is infrastructure, not moat. The moat is what's inside the schema. The editorial decision register, over time, becomes the proprietary asset hardest for a competitor to replicate because it encodes judgment, not just data.

---

## Section 18: Content Neutrality and Framing

### The Principle

All published data is statistical reporting without editorial interpretation. Report what data shows. Document methodology. Acknowledge limitations. Don't advocate, critique, or frame variance as misconduct.

**Why:** Credibility (neutral reporting citable by all parties), data access protection (court administrators can't object to neutral statistics), algorithmic trust (objectivity signals).

**Practical framing:** Correct: "Dismissal rate in County A was 12%, compared to 67% in County B and a statewide average of 43%." Incorrect: "County A's shockingly low dismissal rate suggests overly aggressive prosecution."

### Adjudication Withheld [FIRM DECISION]

Always presented as its own distinct category. Never merged with conviction or dismissal. Three categories minimum: convicted, adjudication withheld, dismissed. Educational explanation included on every page where it appears. The educational value is itself a differentiator.

### Confounding Variable Disclosure [FIRM DECISION]

Required for every demographic or representation-type cross-reference. The COUNSEL_CATEGORY analysis must explicitly state it does not control for pre-trial detention, charge severity, or prior record. Report numbers. State limitations. Don't imply causation.

### Anomalous Findings

Published identically to all other findings. Same formatting, methodology, neutral framing. Don't suppress. Don't sensationalize.
## Section 19: Evidence-Tagged Assumptions Register

### CONFIRMED

1. Florida CJDT provides bulk CSV, 56 confirmed counties, 2018-present, monthly refresh, statutorily mandated (F.S. 900.05)
2. CJDT has 4,092,482 charge records across 55 columns
3. DUI records total ~340,000-350,000, filterable by FCIC_Category or statute code
4. UNIQUE_CORRELATION_ID enables case-level grouping
5. Disposition field 100% populated with 15-16 standardized categories
6. COUNSEL_CATEGORY 100% missing for Broward County
7. No judge identifier in Clerk Case dataset (only Judicial Circuit)
8. Financial fields (FINE, RESTITUTION) >77% missing, unusable
9. 4 counties apparently missing (Brevard, Charlotte, Okaloosa, Sarasota)
10. No competitor other than FCF deploys data-oriented schema on legal content
11. Justia has zero schema on statute pages
12. MFJ has zero schema on data pages, React SPA invisible to crawlers
13. FindLaw's Article + reviewedBy + EducationalOccupationalCredential is pre-FCF E-E-A-T benchmark
14. FCF has Dataset + variableMeasured + FAQPage + BreadcrumbList -- best-in-class data schema
15. FCF ranks #1 organically for long-tail county data queries within 8 days of launch
16. FCF cited in ZERO AI Overviews despite #1 rankings and perfect schema
17. FCF has no named authors, no synthesis, no Tier C, zero backlinks
18. No entity publishes consumer-facing, current, normalized disposition stats with synthesis and editorial quality
19. MFJ last updated January 2022, covers 20 of 50 states
20. Traffic bifurcation: primary source (Justia +11.4%) grows, explanatory (Shouse -51%, Nolo -42.3%) declines
21. Florida uses Adjudication Withheld (~22%) with no direct equivalent in most states
22. 50-state scan: 3 HIGH, 16 MODERATE, 31 LOW
23. AI Overviews appear on 60%+ of all queries, 23-78% of legal queries [REPORTED]
24. AI Overviews reduce organic CTR by 58% when present [REPORTED]
25. 55% of AI Overview citations come from first 30% of page content [REPORTED]

### LOGICALLY DEDUCED

1. Florida is optimal proof-of-synthesis jurisdiction
2. Criminal defense is optimal starting vertical
3. DUI is optimal first charge type (volume, intent, filterability, commercial value)
4. AI citation requires schema + authority + E-E-A-T, built incrementally (from FCF zero-citation finding)
5. Information sequencing serves user intent better than legal content conventions (JTBD analysis)
6. Synthesis-layer content generates more citations than programmatic data pages
7. Partial Tier B enrichment in data-limited jurisdictions clears editorial gate if documented
8. The project functions as an appreciating asset
9. Cohort aggregation solves sample size problem
10. Normalization burden per jurisdiction is substantial; Phase 1 takes longer than expected
11. Contributor value is strengthened by zero-click (high-intent filtering)
12. Net-new defined against FCF at Tier 3; Tier 1 competes on quality and reader benefit
13. 50-state transparency audit is net-new and publishable
14. COUNSEL_CATEGORY cross-reference requires confounding disclosure
15. Editorial decision register becomes proprietary asset over time
16. Pages organized by search behavior outperform pages organized by database structure
17. State-level charge pages with interactive county data better serve readers than county-per-page model
18. Multiple cross-referenced data sources produce exponentially more information gain than single sources
19. The data journalism pipeline (procurement → harmonization → EDA → triage → documentation → publication) is the correct operational model
20. Citability is a trajectory built over time, not a launch metric

### UNVERIFIED / SPECULATIVE

1. California DOJ OpenJustice Portal actual data quality
2. Virginia Court Data sustainability
3. Texas re:SearchTX bulk export capability
4. Colorado compiled data request viability
5. Commercial API cost-effectiveness (UniCourt ~$2,250/month)
6. Contributor conversion rates
7. 6-12 month authority building timeline
8. Zero-click click value multiplier (~3x)
9. FDLE SAO Case Reports dataset field contents
10. DHSMV administrative DUI data obtainability
11. FDLE arrest/UCR data linkage to CJDT
12. Florida DOC data obtainability and linkage
13. FLHSMV crash data linkage to CJDT
14. County jail booking data availability
15. PERSON_ID reliability across counties and time
16. Practice areas beyond criminal defense data availability
17. Refresh/maintenance cost sustainability
18. Phase 1 timeline and cost estimates
19. Proof-of-synthesis producing meaningful county-level variance
20. The 50-state audit generating media interest
21. FCF's future development direction
22. Phase 2+ monetization viability (licensing, dashboards, subscriptions)
23. Optimal trailing window length for temporal windowing
24. Minimum viable sample size thresholds
25. Charge-level vs. case-level metric divergence magnitude

---

## Section 20: Open Questions

### Resolved by Research

- Which jurisdictions have accessible data? → 3 HIGH, 16 MODERATE, 31 LOW mapped.
- Is criminal defense the right vertical? → Yes.
- Who is already doing this? → MFJ (stale, invisible), FCF (programmatic, no synthesis). Full platform thesis unoccupied.
- Schema gap? → Confirmed total except FCF.
- CJDT data structure? → Fully mapped via inspection.

### Phase 1A (Resolve in First 2 Weeks)

**Q1:** What does the actual Florida DUI data reveal? Does statewide disposition produce numbers that are net-new? Does cross-county variance reveal meaningful findings?

**Q2:** What's in the FDLE SAO Case Reports dataset? Download and inspect week 1.

**Q3:** What's the actual divergence between charge-level and case-level metrics? Calculate both, compare. If <5 points, low-stakes framing choice. If >15 points, high-stakes.

**Q4:** What percentage of Florida's DUI case volume is in the 4 absent counties? Determines whether "statewide" framing is defensible.

**Q5:** Which counties have good COUNSEL_CATEGORY coverage for DUI? Determines where representation-type cross-reference is buildable.

**Q6:** Is PERSON_ID reliable across counties and time? BLOCKER for situational pages. Validate week 1.

**Q7:** What trailing window length produces stable but current statistics? Compute rates at 1/2/3-year windows, observe stability.

**Q8:** What sample size thresholds produce reliable county-level statistics? Observe volatility at varying N.

**Q9:** Which situational filters can be cleanly applied? First offense (PERSON_ID), felony (Level), specific subsections -- which produce defensible subsets?

**Q10:** What's the technical approach for the interactive county element? Build prototype, validate LLM readability.

**Q11:** How many counties meet the three conditions for standalone pages?

**Q12:** Does schema validate on prototype pages with full county JSON-LD? Test density limits.

**Q13:** What other FCIC categories in CJDT are well-populated? Catalog for expansion.

**Q14:** What secondary sources (SAO, DHSMV, UCR) are accessible? Quick investigation, parallel track.

### Phase 1B+ (Resolve During Build-Out)

**Q15:** Charge-to-statute mapping for non-DUI practice areas.

**Q16:** Expansion state data inspection (California, Virginia first).

**Q17:** ToS and redistribution restrictions for expansion states.

**Q18:** Entity structure (LLC, nonprofit, etc.) -- liability, credibility, data access implications.

**Q19:** At what point does System Coherence transition from augmentation to structural? (Likely ~100-200 pages.)

**Q20:** How are reader models encoded into the agentic pipeline?

---

## Section 21: Phase Sequencing

### Pre-Phase-1 Checklist

1. Phase 1 kill triggers defined (see below)
2. Editorial decision register schema defined (Section 9)
3. FIRM: Adjudication Withheld always separate
4. FIRM: Confounding variable disclosure on all demographic/representation cross-references
5. FIRM: No named attorney required at launch
6. FIRM: Pages organized by search behavior, not database structure
7. FIRM: Priority stack (Reader Benefit → LLM Readability → Net-New)

### Phase 1 Kill Triggers

- If statewide DUI disposition produces numbers a practicing attorney would immediately call wrong
- If more than 20% of counties have data quality issues requiring individual investigation
- If every proposed net-new synthesis or cross-reference already exists on FCF in equivalent form
- If schema validation fails on prototype pages
- If PERSON_ID is unreliable and no alternative methodology for situational filtering is viable

### Phase 1A: Rapid Validation (2 Weeks)

**Week 1 priorities (blocking items first):**
- Download CJDT Clerk Case data, load database, verify against data dictionary
- Download and inspect SAO Case Reports dataset
- Validate PERSON_ID reliability (BLOCKER for situational pages)
- Extract DUI subset, verify record count and filtering
- Calculate statewide DUI disposition distribution
- Calculate BOTH charge-level AND case-level metrics, compare divergence
- Quantify missing county coverage gap
- Check COUNSEL_CATEGORY population by county, rank by DUI volume × completeness
- Quick investigation: SAO field contents, DHSMV accessibility, UCR data availability

**Week 2 priorities:**
- Calculate top-10-county breakdown, identify meaningful variance
- Test trailing window lengths (1/2/3 year), observe stability
- Determine sample size thresholds from observed volatility
- Build prototype CHARGE PAGE (not county page) with interactive county element
- Apply full schema stack, validate against Rich Results Test
- Test technical approach for interactive county element and LLM readability
- Catalog other well-populated FCIC categories for expansion
- Submit prototype to Search Console

**Phase 1A success criteria:**
1. Data is real, verified, properly sourced
2. Synthesis produces findings or cross-references not on FCF
3. Cross-county comparison reveals meaningful variance
4. Schema validates
5. Prototype charge page serves reader intent per the inclusion matrix
6. Structure is fully LLM-parseable
7. Quality meets "attorney would put name on it, journalist would cite it" standard

**Phase 1A is NOT measured by:** AI Overview citation, organic traffic, CTR, Search Console impressions. Monitored for information. Do not determine success.

### Phase 1B: Full Build-Out (2-4 Weeks)

- Remaining cross-references: co-occurrence, temporal trends, representation type (confounding disclosure), severity
- MFJ historical baseline comparison
- Situational page production (where data supports clean filtering)
- Conditional county page evaluation (three conditions)
- Editorial decision register: log every judgment
- Seed content: 20-50 pages, quality over quantity
- Cost/timeline profile
- Legal disclaimer framework (attorney review)
- 50-state transparency audit polished for publication
- Secondary source investigation results inform enrichment roadmap

### Phase 2: Publication

Florida data pages and 50-state transparency audit published simultaneously. Audit says "here's the landscape." Pages say "here's what we built." Complete story from day one.

### Phase 3: Authority Verification (60-90+ Days)

Monitor ranking, citation, backlinks. Domain sandbox expected. Zero citation at 60 days is expected, not failure. 6-month checkpoint: if zero citation, diagnostic review (not kill trigger -- review trigger).

### Phase 4: Jurisdiction Expansion

Follow the data. California and Virginia first candidates (need inspection). Each state reuses pipeline with jurisdiction-specific normalization. Begin Tier 3 cross-jurisdictional synthesis.

### Phase 5: Contributor Recruitment

After pages rank and traffic demonstrated. Statute-matched outreach.

### Phase 6: Practice Area and Vertical Expansion

Criminal defense → family law, personal injury, etc. Long-term: the architecture is domain-agnostic. Healthcare, financial, tax, building codes, environmental compliance.

---

## Section 22: Firm Decisions, Open Decisions, Not-Converged Items

### Firm Decisions (Made, Not Revisited)

1. Adjudication Withheld always a separate category
2. Confounding variable disclosure on all demographic/representation cross-references
3. No named attorney required at launch (schema ready, empty until Phase 2+)
4. Priority stack: Reader Benefit → LLM Readability → Net-New
5. Pages organized by how people search, not by database structure
6. County-level data is an interactive feature within state-level pages, not separate URLs
7. The editorial gate escalates by tier: Tier 1 = quality/structure/reader benefit; Tier 2 = expected net-new; Tier 3 = mandatory net-new with full gate
8. Content neutrality is non-negotiable
9. Citability is a trajectory, not a launch metric
10. The data journalism pipeline (procurement → harmonization → EDA → triage → documentation → publication) is the operational model

### Open Design Decisions (Resolve During Phase 1)

1. Charge-level vs. case-level canonical metric (calculate both, compare divergence, pillar framework decides)
2. Trailing window length (calibrate from data stability analysis)
3. Minimum sample size thresholds (calibrate from data volatility observation)
4. "Meaningful differentiation" threshold for conditional county pages (calibrate from observed variance)
5. Technical approach for interactive county element (prototype and test)
6. Site architecture (static, server-rendered, hybrid -- operator preference + technical constraints)
7. Domain and branding
8. Demographic data presentation depth (include in template, decide visibility timing)
9. Visualization technical approach (SVG + structured data vs. JSON-LD companion vs. accessible table)
10. Per-block schema annotation scope (page-level vs. block-level)

### Not Converged (Deferred to Data)

- Specific trailing window length
- Specific sample size thresholds
- Specific county page inventory
- Specific situational page inventory (depends on filter feasibility)
- Charge-to-statute mappings for non-DUI practice areas
- Secondary source obtainability and linkage viability
- PERSON_ID reliability
- SAO dataset field contents

---

## Section 23: Risk Registry

**Risk 1: Data Access Bottleneck.** PARTIALLY RESOLVED. Florida confirmed. Others mapped.

**Risk 2: HCU Classification.** Programmatic legal content at scale may trigger thin-content evaluation. Mitigation: editorial gate, quality standard, Reader Benefit pillar. FCF's 4,500 programmatic pages are the reference point for what this project must exceed.

**Risk 3: Contributor Cold Start.** 6-12 months zero revenue. [UNVERIFIED timeline.]

**Risk 4: Link Scheme Classification.** Quality gate on contributions is load-bearing.

**Risk 5: Premature Scaling.** Deep before wide. 20 excellent pages, not 50 adequate.

**Risk 6: Normalization Errors.** Normalization Authority Protocol. Legal SME review. Unmappable designations. EDA stage catches errors before publication.

**Risk 7: Competition.** FCF is direct competitor. MFJ institutional analog. Neither occupies full platform thesis. [CONFIRMED]

**Risk 8: Political Sensitivity.** Content neutrality. Acceptable degradation if data access cut.

**Risk 9: Legal Liability.** Statistical reporting, not advice. Attorney disclaimer review.

**Risk 10: Data Licensing.** Florida statutory mandate -- strongest position. Others uninvestigated.

**Risk 11: Bootstrapping Economics.** Unknown costs until Phase 1.

**Risk 12: Domain Sandbox.** [CONFIRMED] Expected operating condition. E-E-A-T and authority build over time.

**Risk 13: FCF Iteration.** Could build synthesis layers. Lead-gen incentives make unlikely.

**Risk 14: PERSON_ID Reliability.** If unreliable, situational pages and several cross-references need alternative methodology. Phase 1A blocker. Validate week 1.

**Risk 15: Multi-Source Linkage Failure.** Cross-referencing datasets that lack common identifiers produces aggregate-only analysis. Lower information gain than case-level linkage. Mitigation: the EDA stage validates linkage before publication. Aggregate analysis is still valuable (honest about granularity).

**Risk 16: Schema Processing Changes.** Google could change how it evaluates structured data. Mitigation: prioritize proven types (Dataset, FAQPage) over experimental (StatisticalVariable). Content quality and Reader Benefit hold value independent of schema changes.

---

## Section 24: Critical Principles

**0. The priority hierarchy governs all content decisions.** (1) Serve reader intent, (2) LLM-readable and genuinely helpful to machine, (3) net-new and citable. Lower priorities never override higher.

**1. Data earns the page -- tiered.** Tier 1: quality, structure, reader benefit. Tier 2: expected net-new from aggregation. Tier 3: mandatory net-new with full editorial gate (intent, data says something, comparison valid).

**2. Be the source, not the destination.** Citation authority is the terminal metric. Structural citability is the launch metric. Citability is a trajectory, not a launch metric.

**3. Transparency is the trust architecture.** Published methodology, sample sizes, limitations, normalization rules. The methodology IS the credibility. Our World in Data model.

**4. Content neutrality is non-negotiable.** Report statistics. Disclose confounders. Don't advocate.

**5. Avoid the dead man's zone.** No generic comparisons confirming expected patterns.

**6. Deep before wide.** Dominate one state before expanding. 20 excellent pages over 50 adequate.

**7. The pipeline is a data journalism pipeline.** Procurement → harmonization → EDA → editorial triage → documentation → publication. Not an SEO content pipeline.

**8. Handle jurisdiction terminology explicitly.** Document every normalization decision. Legal SME review. Unmappable designations permitted.

**9. First manually, then agentically.** First jurisdiction is manual. Edge cases make the pipeline correct. Phase 1 takes longer than planned.

**10. The editorial gate is non-negotiable at Tier 3.** Intent exists, data says something, comparison structurally valid. All three.

**11. Schema is infrastructure, not moat.** Schema makes other layers machine-readable. The moat is what's inside the schema.

**12. Pages organized by search behavior, not database structure.** County-level data in the database does not require county-level URLs. Data existence and page existence are independent decisions.

**13. AI citation requires schema + authority + E-E-A-T -- built incrementally.** Not required simultaneously at launch. Phase 1 delivers schema. Authority and E-E-A-T accumulate.

**14. Everything compounds.** Each data point enriches every tier. Each citation reinforces authority. Non-linear value.

**15. This is an appreciating asset.** Content depreciates. Data appreciates. Build data with a content interface.

**16. Coverage follows the data.** Expansion by accessibility, not geography. Irregular coverage is honest.

**17. Make it stupidly obvious for machines.** Structure so LLMs unambiguously identify what data represents, where it's from, why to trust it.

**18. Tag your confidence.** Every claim has an evidence level. Don't treat speculation as fact.

**19. Define failure conditions before starting.** Kill triggers prevent sunk-cost escalation.

**20. The legal vertical is the first instantiation.** Architecture is domain-agnostic. Pipeline transfers to any domain with fragmented public data.

**21. Multi-source cross-referencing is the ultimate information gain.** One source = statistics. Two = cross-references. Three+ = findings that can't exist elsewhere.

**22. The negative space is a design decision.** What's excluded from a page is as important as what's included. Data topically relevant but not beneficial to THIS reader at THIS tier is noise.

**23. The reader-LLM distinction operates in different layers.** Visible content governed by Reader Benefit. Machine structure governed by Machine Confidence. Adding visible content "for the LLM" violates Reader Benefit. Adding invisible schema does not.

**24. The old SEO paradigm does not apply.** Traffic volume is not the metric. Citation authority is. Declining traffic at explanatory sites is validating, not alarming. Discovery is through citation, not ranking.

---

## Section 25: Where Other LLMs Consistently Get It Wrong

These are recurring correction patterns observed across multiple LLM reviews. Any LLM working on this project should internalize these before providing advice.

**1. Defaulting to traffic-volume concerns.** Flagging "930-3,340 monthly searches" as insufficient demand. Wrong paradigm. The project doesn't depend on explicit data query searches. It depends on AI citing this data across millions of DUI-related queries.

**2. Treating FCF as a competitive threat rather than validation.** FCF proves the technical thesis, proves organic ranking, and proves schema alone doesn't get AI citations. Their existence removes first-mover on basic statistics but that was never the moat. FCF's lead-gen incentives push toward more pages and forms, not deeper synthesis.

**3. Over-weighting political sensitivity.** Elaborate protocols for anomalous findings. The operating position: publish neutral statistics. If someone is upset about their county's numbers, the data is public and the framing is neutral.

**4. Suggesting anti-extraction mechanisms.** Engineering content to prevent AI from extracting value. The depth driving click-through is natural. Building extraction barriers is adversarial to the distribution mechanism.

**5. Recommending against Tier 1 pages.** "Skip to Tier 3 synthesis." Tier 1 pages are data infrastructure, internal linking anchors, and where the per-county reader lands. They need to exist. They just need to be better than what's available, which they are via information sequencing and schema.

**6. Over-planning expansion before Phase 1.** Detailed 50-state strategies and multi-year projections. Florida first. Prove the thesis. Everything else is background context.

**7. Defaulting to per-page novelty gate at Tier 1.** The editorial gate escalates by tier. Tier 1 competes on quality, structure, and reader benefit. Net-new is the aspiration, not the gate. Net-new is mandatory only at Tier 3.

**8. Treating E-E-A-T attorney as launch requirement.** Creates circular dependency. Can't recruit attorneys to zero-authority platform. Schema connection points built. Empty at launch. Filled Phase 2+.

**9. Evaluating contributor model on click volume.** The value is canonical source association, not clicks. Clicks are a bonus. The contributor appears on the page AI attributes.

**10. Applying old-paradigm SEO thinking generally.** Monthly visits, keyword targeting, traffic capture, competitive ranking position. None of these are the primary metric. Citation authority is. The paradigm is different. Internalize it before advising.
