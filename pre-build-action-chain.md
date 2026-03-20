# Pre-Build Action Chain

**Date:** March 20, 2026
**Purpose:** Everything that needs to happen before the first page is built, in what order, why, and where it might deviate.
**Companion to:** Project Handoff Report (read that first for full project context)

---

## Step 1: Query Environment Setup

**What it is:** Load the CJDT Clerk data (and SAO data) into a proper database — PostgreSQL, DuckDB, SQLite, whatever you're comfortable with. Write the core filter queries (DUI statute filter, 2023-2025 window, conviction filter) as saved, version-controlled queries you can re-run.

**Why it's first:** Everything downstream depends on trustworthy numbers. Manus gave us directional findings, but every key number needs re-running in an environment where you can inspect the query logic, verify edge cases, and reproduce results. One misinterpreted filter condition could cascade through every page.

**What "done" looks like:** You can run a query, get a result, inspect the SQL/code that produced it, and re-run it tomorrow and get the same answer. The DUI statute filter is documented and tested. You've confirmed record counts match what Manus reported (or identified where they differ and why).

**What could change this sequencing:** If you have a preferred tool or workflow already (like a local Python + DuckDB setup, or Claude Code with the CSV), this could be done in an hour. If you need to evaluate tools first, it takes longer but is still step 1 regardless.

---

## Step 2: Verify Critical DUI Findings

**What it is:** Re-run the 5-6 queries that produced our most important findings, in the new environment. Specifically:

- Statewide DUI disposition distribution (do we still get 93.4%?)
- Jail classification for Duval, Pinellas, and 2-3 other counties (does the booking artifact pattern hold?)
- Financial burden for top counties (does the $931-$2,912 range hold?)
- Non-conviction pathways for Orange County (is it really 40.9%?)
- One FCF cross-check (pick Hernando — do we still match their 651 cases?)

**Why it's second:** These findings are the foundation of the entire content strategy. If the jail classification is wrong, our core differentiator is wrong. If the financial burden numbers shift significantly, our page content changes. We built an entire framework on these numbers — verifying them before building on them further is basic due diligence.

**Why not verify everything:** We don't need to re-run all 42 county classifications right now. We need to confirm the methodology works on a handful, then run the full set when we're actually populating pages. Verification should be proportional to how close we are to publishing.

**What could change this sequencing:** If verification reveals significant discrepancies from Manus output, that's a detour. We'd need to diagnose why (filter logic? date handling? null treatment?) before proceeding. If everything confirms, this step is fast and just builds confidence.

---

## Step 3: Search Demand Validation

**What it is:** Keyword research on the actual queries people use around DUI in Florida. Not comprehensive SEO keyword mapping — targeted validation of our assumptions about what pages to build and what people actually search.

**Why it matters:** We built the page architecture from first-principles reader modeling ("what would a person in this situation search for?"). That's probably directionally right, but we might be wrong about which situational pages have real demand. Maybe "DUI refusal Florida" gets significant search volume and "felony DUI Florida" doesn't. Maybe "DUI cost Florida" is a massive query nobody's serving well. This data directly affects which pages we prioritize building first.

**Why it's before building, not during:** Page titles, URL structure, and content framing all depend on understanding how people actually phrase their searches. Building a page called "DUI Refusal in Florida" when everyone searches "what happens if you refuse breathalyzer Florida" means we'd need to restructure later. Cheaper to know now.

**What this is NOT:** A full SEO audit. A competitive keyword gap analysis. A traffic projection model. It's 2-3 hours of keyword tool work to validate or adjust our page inventory and prioritize the build order.

**What could change this sequencing:** This could run in parallel with Steps 1-2. It's not dependent on verified data — it's about search behavior, not our numbers. If you want to move faster, do this simultaneously.

---

## Step 4: Battery Profiling

**What it is:** Run the same profiling pipeline on Battery (784.03) that we ran on DUI. Disposition distribution, sentencing patterns, booking artifact check, financial field coverage, DV indicator analysis, co-occurrence, statute mapping decision.

**Why it's here and not later:** This isn't about building Battery pages yet. It's about confirming the framework generalizes before we invest heavily in building DUI pages based on that framework. If Battery reveals that the block library is missing critical components, or that the situational discovery process doesn't work for non-DUI charges, we want to know before we've built 10 DUI pages on assumptions that don't hold.

**The specific things this tests:**
- Does the booking artifact pattern exist for non-DUI arrests?
- Does the DV indicator at 63% populated actually produce useful splits?
- Is the statute mapping problem solvable (Battery has 31 statute strings)?
- Does the editorial story differ meaningfully from DUI? (We expect it will — AW and diversion should dominate instead of sentencing.)

**What "done" looks like:** A profiling report similar to what Manus produced for DUI, plus a short assessment of what transfers from the DUI framework and what needs adjustment.

**What could change this sequencing:** If you'd rather go deep on DUI and ship those pages before touching Battery, this moves to post-first-build. The risk is discovering framework problems after you've built on assumptions. The benefit is focus. Your call on risk tolerance.

---

## Step 5: Diversion Program Research

**What it is:** Map which Florida counties have formal DUI diversion programs — name, basic eligibility, what it involves (charge reduction to reckless, requirements like DUI school and community service, typical duration). We know RIDR (Hillsborough) and DROP (Pinellas). There are likely 10-20 more.

**Why it matters:** This is one of the highest reader-benefit content elements. A person in Orange County (28.7% diversion rate) needs to know that program exists and what it involves. This is the kind of information that genuinely changes what the reader does — they ask their attorney about diversion eligibility, which they might not have known to ask about.

**Why it's before building:** The diversion information goes directly into multiple pages (hub charge page, first offense page, county pages). If we build those pages without it, we leave out one of the most useful elements and have to retrofit later.

**What this is NOT:** A comprehensive legal analysis of each program. It's a research pass: which counties have programs, what are they called, what are the basic published eligibility criteria. Detailed program analysis is Phase 2 / contributor content territory.

**What could change this sequencing:** This can run fully parallel with everything else. It's research, not data work. Could be a Manus task, manual research, or both.

---

## Step 6: Schema Density Test

**What it is:** Build a mock JSON-LD block at the density the hub charge page would require (statewide Dataset + county datasets + FAQPage + Article + ClaimReview) and test it against Google's Rich Results Test and Schema.org validator.

**Why it's before building:** If the JSON-LD is too large or complex for validators to handle, the entire schema strategy needs adjustment. Better to discover this with a test payload than after building real pages. The fallback hierarchy is defined (Working Notes Part 10) but we'd rather not need it.

**Fallback hierarchy if it fails:**
1. Statewide Dataset + FAQPage first (proven citation drivers)
2. County data in separate linked Dataset referenced by @id
3. ClaimReview limited to top 2-3 findings per page

**What "done" looks like:** A JSON-LD block at production density, validated. Either it passes (green light) or it fails and we implement the fallback hierarchy before building pages.

**What could change this sequencing:** This is a few hours of work and could be done any time before the first page is built. It's not dependent on verified data — you can use placeholder numbers. But it IS a blocker for the build, so doing it earlier reduces risk.

---

## Step 7: Domain, Branding, Legal Entity

**What it is:** Register a domain. Decide on the site name. Set up the business entity (LLC or similar). Get a basic legal disclaimer reviewed.

**Why it's here:** None of this blocks the data or content work, but it blocks going live. It's also the kind of decision that's easy to overthink. The domain and name should reflect the platform's positioning (data authority, not attorney marketing) but doesn't need to be perfect — it needs to be defensible and available.

**Why the legal disclaimer matters:** We're publishing statistical data about criminal case outcomes. The disclaimer that this is statistical reporting, not legal advice, needs to be solid. An attorney review of the disclaimer is not optional — it's a liability protection requirement.

**What could change this sequencing:** This runs in parallel with everything. No dependencies in either direction. But it does need to happen before anything goes public.

---

## Step 8: Tech Stack Decision

**What it is:** Decide how pages are built and served. The CourtFile validation suggests server-side Python rendering is the proven pattern for this use case (FastAPI + templates). But our pages have more complexity (interactive county element, editorial content, interpretation layer). The decision space is roughly: static site generator, server-side rendered app, or hybrid.

**Why it's after content work but before building:** The tech stack should serve the content requirements, not the other way around. Once we know what the pages need to contain (verified data, interactive elements, schema density), the tech choice becomes clearer. Deciding tech before content is how you end up rebuilding.

**Key constraint from V5:** You don't want to be troubleshooting heavy tech issues. Simple and reliable beats clever.

**What could change this sequencing:** If you already have strong preferences or an existing technical setup, this decision can happen earlier. 

---

## Step 9: Build Prototype of Hub Charge Page

**What it is:** The first real page. DUI in Florida. Full content with verified data. Interactive county element. Complete schema stack. Real methodology documentation. This is the proof of concept.

**Why it's the first build target:** It's the most complex page (if this works, everything simpler works too), it's the highest-traffic entry point, and every other page references it. Building a situational page first would mean building without the hub it links to.

**What "done" looks like:** A page a practicing attorney would put their name on and a journalist would cite. Verified data, interpreted metrics, county interactive with correct classification templates, honest methodology, proper schema, passes Rich Results Test.

---

## Dependency Map

```
SEQUENTIAL (each blocks the next):
  Step 1 (query env) → Step 2 (verify data) → Step 9 (build prototype)

PARALLEL TRACK A — can start immediately, informs build:
  Step 3 (search demand validation)

PARALLEL TRACK B — can start immediately, tests framework:
  Step 4 (battery profiling)

PARALLEL TRACK C — can start immediately, feeds into content:
  Step 5 (diversion program research)

BLOCKERS FOR BUILD (must clear before Step 9):
  Step 6 (schema density test)
  Step 8 (tech stack decision)

BLOCKERS FOR PUBLISH (must clear before going live):
  Step 7 (domain / legal entity / disclaimer)
```

Visual:
```
Step 1 ──→ Step 2 ──────────────────────→ Step 9 (BUILD)
                                            ↑  ↑  ↑
Step 3 (search demand) ────────────────────┘  │  │
Step 5 (diversion research) ──────────────────┘  │
Step 6 (schema test) ────────────────────────────┘
Step 8 (tech stack) ─────────────────────────────┘

Step 4 (battery profiling) ──→ framework confidence (informs build approach)
Step 7 (domain/legal) ──→ blocks PUBLISH, not build
```

---

## Deviation Scenarios

**"I want to move faster":**
Collapse Steps 1-2 into a single session (set up database AND verify key findings in one pass). Skip Step 4 (Battery profiling) for now and go straight to building DUI pages, accepting the risk that the framework might need adjustment later. Run Steps 3, 5, 6 in parallel.

**"I want more confidence before building":**
Add a step between 2 and 9: run the full 42-county jail classification in the verified environment, plus financial burden for all counties, plus non-conviction pathways for all counties. This gives you the complete data layer before building but adds time.

**"Schema test fails":**
Creates a detour where you redesign the JSON-LD structure before building. Could add a day or could add a week depending on severity. The fallback hierarchy is defined — implement it and proceed.

**"Search demand reveals unexpected patterns":**
Might reshuffle which pages get built first. Could promote a situational page above the hub if the data shows that's where the real search volume is. Could reveal query phrasings that change page titles and URL structure.

**"Verification reveals discrepancies from Manus":**
Detour to diagnose why (filter logic? date handling? null treatment?). If the core findings hold but numbers shift slightly, no problem — update the working notes and proceed. If a major finding reverses (e.g., the booking artifact pattern doesn't hold), that requires rethinking the content strategy before building.

**"Battery profiling reveals framework problems":**
If the block library is missing critical components for non-DUI charges, add them before building DUI pages (since the library is supposed to be charge-type-agnostic). If the discovery process doesn't work, adjust the framework. Better to learn this early than after shipping 10 DUI pages.

**"I just want to start building and figure things out as I go":**
Steps 1 and 2 are still non-negotiable — you cannot build pages with unverified data when your entire value proposition is data accuracy. But Steps 3-8 could be compressed or deferred, with the understanding that you'll likely need to adjust pages after the fact when those steps eventually happen.
