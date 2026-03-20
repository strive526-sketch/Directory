# Build Sequence -- Legal Data Synthesis Platform

**Date:** March 20, 2026
**Status:** Pre-build planning
**Purpose:** Step-by-step sequencing for building the platform. Written so that any LLM assisting with implementation understands the order, reasoning, and dependencies. The project owner has basic HTML/CSS knowledge, strong prompt engineering skills, and prefers to minimize troubleshooting technical issues.

**Companion document:** Read `technical-architecture-report.md` first for the full architectural context and reasoning behind decisions referenced here.

---

## How To Use This Document

This is a sequenced task list, not a tutorial. Each phase describes what needs to happen, why it's in this order, and what the output should be. The project owner will work through these phases with LLM assistance (agentic coding tools like Claude Code, Cursor, or similar).

**Key principle:** Each phase produces a testable artifact. You can verify each phase worked before moving to the next. There are no phases where you do a lot of work and then discover at the end that something fundamental is broken.

---

## Phase 0: Schema Density Test (BLOCKER -- DO THIS FIRST)

### Why This Is Phase 0

The entire structured data strategy depends on whether Google's Rich Results Test accepts the schema density planned for the charge pages. If it doesn't, the URL architecture and component design need to change before anything gets built. Testing this takes ~30 minutes and prevents potentially rebuilding components later.

### What To Do

1. Create a single static HTML file (plain HTML, no Astro needed) that contains:
   - A representative charge page's content (can be placeholder text)
   - The maximum JSON-LD block you'd want: Article + Dataset (statewide) + FAQPage (5-8 questions) + ClaimReview (2-3 claims) + at minimum 10 county-level Dataset entries

2. Test against:
   - Google Rich Results Test (https://search.google.com/test/rich-results)
   - Schema.org Validator (https://validator.schema.org/)

3. Record results:
   - If both pass cleanly: proceed with dense schema on charge pages. No architectural changes needed.
   - If Rich Results Test warns or fails on density: implement fallback hierarchy (statewide schema on page, county data at separate URLs). This affects URL structure -- decide before Phase 2.

### Output

A documented result: "Schema density test passed/failed on [date]. [If failed: fallback hierarchy in effect, county data will live at /data/ endpoints.]"

---

## Phase 1: Environment Setup

### 1A: Local Development Environment

**Install Node.js.** Astro requires Node.js 18+. Download from nodejs.org. Verify with:

```bash
node --version   # Should show v18.x or higher
npm --version    # Should show 9.x or higher
```

**Install Git.** Download from git-scm.com, or install GitHub Desktop (which includes Git). Configure:

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

**Install a code editor.** VS Code is recommended -- it has Astro syntax highlighting via the official Astro extension, integrated terminal, and Git integration. Cursor is an alternative if you prefer AI-native editing.

### 1B: Create The Astro Project

```bash
npm create astro@latest legal-data-platform
cd legal-data-platform
npm run dev
```

This scaffolds a fresh Astro project and starts the local development server. You should see a welcome page at `http://localhost:4321`. If this works, your environment is functional.

**Install the sitemap plugin:**

```bash
npx astro add sitemap
```

### 1C: Create GitHub Repository

1. Create a new repository on GitHub (private initially, can make public later)
2. Connect local project to GitHub:

```bash
git remote add origin https://github.com/yourusername/legal-data-platform.git
git add .
git commit -m "initial astro project"
git push -u origin main
```

Or use GitHub Desktop: Add > Existing Repository > select project folder > Publish.

### 1D: Connect to Cloudflare Pages (or Netlify)

**Cloudflare Pages:**
1. Sign up at pages.cloudflare.com
2. Create new project > Connect to Git > Select your repository
3. Build settings: Framework preset = Astro, Build command = `npm run build`, Output directory = `dist`
4. Deploy

**After this step:** Every `git push` to main automatically builds and deploys. Verify by making a small change to the welcome page, pushing, and confirming it appears on your Cloudflare URL within 1-2 minutes.

### 1E: Custom Domain (Can Be Deferred)

Purchase domain through your preferred registrar. In Cloudflare Pages (or Netlify), add custom domain and update DNS records as instructed. SSL is automatic.

**This can wait until content is ready.** The Cloudflare/Netlify auto-generated URL works for development and testing.

### Output

A working Astro project, connected to GitHub, auto-deploying to a CDN. You can edit a file, push, and see it live. This is the deployment pipeline that will serve the entire project.

---

## Phase 2: Project Scaffolding

### Why This Phase Exists

This is the "build the frame of the house" phase. You create the directory structure, base layouts, and empty component files. No real content yet -- just the skeleton that everything else plugs into. This is the most technical phase and the one where you'll lean most heavily on LLM coding assistance.

### 2A: Create Directory Structure

Set up the folder structure as defined in the technical architecture report (Section 3). Create all directories and placeholder files. An LLM can generate this entire structure from the architecture doc in one prompt.

### 2B: Build BaseLayout.astro

The base layout handles everything shared across all pages:
- HTML `<head>` with meta tags, SEO defaults, schema injection slot
- Navigation component
- Main content area (`<slot />` -- this is where page content goes)
- Footer component
- Global CSS link

Also during this step:
- Install `@astrojs/rss` plugin alongside the sitemap plugin. Configure RSS to include BLUF text and data summaries per entry, not just titles and links (see architecture report Section 11).
- Configure the sitemap plugin with explicit priority values: charge hub pages at `priority=1.0`, methodology at `0.8`, situational pages at `0.7`, static pages lower.
- Create `/public/robots.txt` with explicit `Allow` directives for AI crawler user agents: GPTBot, ClaudeBot, PerplexityBot, Applebot-Extended, CCBot.
- Create `/public/_headers` file with `X-Robots-Tag: all` header for Cloudflare Pages to serve on all responses.

**Test:** Create a simple test page that uses BaseLayout. Verify nav, footer, and content area render correctly at `localhost:4321`.

### 2C: Build ChargePage.astro Layout

This is the layout that reads the `blocks` frontmatter array and renders components in order. This is the core assembly mechanism described in the architecture report (Section 4).

**Implementation approach:**
1. Start with a hardcoded layout that just renders Markdown content (no block system yet)
2. Add the block registry and mapping logic
3. Test with a dummy page that lists 2-3 placeholder blocks

**Test:** A Markdown file with `blocks: [{type: "bluf"}, {type: "faq"}]` in frontmatter renders both components in order.

### 2D: Global CSS and Design Token System

Define the CSS custom properties (design tokens) in `variables.css` as specified in the architecture report (Section 10). This is the foundation every component references. Without it, each component will drift into its own spacing, colors, and type sizes -- creating inconsistency that's painful to fix retroactively.

The token system covers:
- Typography scale (body, headings, small text, captions)
- Spacing scale (consistent increments from 4px to 64px)
- Color palette (text, backgrounds, borders, semantic colors for confidence tiers)
- Border radii and shadows
- Content max-width and page padding
- Responsive breakpoints (mobile-first; most readers are on phones at 2 AM)

Also define base table styling, link styling, and global typography here. Keep it minimal. The site's design identity is "clean data presentation," not "creative design."

**This must be done before the next step.** Every styled element should reference tokens from day one. The specific values are adjustable later; the structure is what matters.

### 2E: Build UI Components (Styled Elements)

These are the reusable styled building blocks that content blocks use. All should reference the design tokens from 2D:
- `CalloutBox.astro` -- bordered box with optional heading, supports style variants (primary, highlight, warning)
- `DataTable.astro` -- clean table with consistent styling, supports caption and source citation
- `InterpretationNote.astro` -- styled aside for editorial commentary on data
- `CaveatBanner.astro` -- prominent caveat/warning display
- `ConfidenceBadge.astro` -- visual indicator for high/moderate/low confidence
- `SourceCitation.astro` -- consistent formatting for data source attribution

**Approach:** Design these as a mini style guide. Each should look clean and professional in isolation. LLM can generate initial versions; you review and adjust styling.

**Test:** Create a style guide page (`/styleguide`) that renders every UI component with sample content. This becomes your visual reference and your check-your-work page.

### Output

A functioning skeleton: base layout renders, charge page layout assembles blocks from frontmatter, UI components are styled and visible on a style guide page. No real data, no real content -- just the frame.


---

## Phase 3: Data Preparation and JSON Creation

### Why This Phase Starts Early

**Phase 3A (the analytical work) has zero technical dependencies.** You don't need Astro installed, you don't need a repo, you don't need anything from Phase 1 or 2 to start cleaning, verifying, and computing your DUI data. This is the bottleneck for the entire project -- the site's value proposition rests on verified, interpreted numbers, and that verification work is unbounded in a way the technical build isn't.

**Start 3A as soon as possible, in parallel with Phase 1.** The JSON file creation (3B) and validation script (3C, 3D) need the scaffolding from Phase 2 to test against, but the underlying analytical work can and should begin immediately.

### 3A: Finalize DUI Data Analysis

This is the work described in the project handoff report under "Data Verification." The raw CJDT data needs to be cleaned, filtered, calculated, and classified. This work happens in whatever analytical environment you're comfortable with -- spreadsheets, notebooks, LLM assistance.

**Required outputs per county (for DUI Florida):**
- Total convictions (2023-2025)
- Jail rate
- Jail classification (booking-artifact / real-jail / mixed) based on documented criteria
- Jail metrics: median sentence days, % 1-2 day sentences, CTS coverage, % 31+ day sentences
- Financial: median total, fine median, court cost median, field coverage %
- Non-conviction: total rate, diversion rate, dismissal rate, AW rate
- Sample size
- Confidence tier
- Display tier (full / limited / suppressed)
- Caveats (if any)

**Plus statewide aggregates and comparison narratives.**

Refer to the V5 working notes (Parts 1, 5, 6B, 9) for the analytical methodology already developed. The `decisionLog` field in the JSON should capture all thresholds and criteria applied.

### 3B: Create dui-florida.json

Convert your analytical output into the JSON structure defined in the architecture report (Section 5). An LLM can do this conversion from a structured spreadsheet export -- provide it the spreadsheet data and the target JSON structure, and it will produce the file.

**Validate:** Run the JSON through a JSON validator (jsonlint.com or VS Code's built-in validation) to catch syntax errors.

### 3C: Create JSON Schema Contract

Write the schema contract file (`charge-type.schema.json`) that defines required fields and types. This is a one-time setup that protects all future data files.

### 3D: Write Validation Script

A simple Node.js script that reads each JSON file in `/src/data/` and validates it against the schema contract. Wire this into the Astro build process so it runs automatically before every build.

**The script should check two things:**
1. **Structural validation:** All required fields present, correct types, no misspellings. This catches data errors.
2. **dateModified / lastUpdated freshness:** Reject any JSON where `lastUpdated` is older than a configurable threshold (e.g., 14 months). On a YMYL domain, a stale `dateModified` in the schema actively signals to AI evaluation systems that the data may be outdated. This should be enforced by the build, not left to manual discipline. The threshold is deliberately longer than the planned refresh cycle to allow buffer, but short enough to catch if a refresh is forgotten.

**Test:** Deliberately break a field in the JSON (misspell a key, remove a required field). Verify the build fails with a clear error message. Then set `lastUpdated` to a date >14 months ago. Verify that also fails. Fix both. Verify the build succeeds.

### Output

A validated `dui-florida.json` file that contains every number the DUI Florida pages will display, with confidence tiers, caveats, display tiers, comparison narratives, FAQ content, and the decision log. A schema contract and validation script that catches both structural data errors and staleness issues in all future JSON files.


---

## Phase 4: Content Block Components

### Why This Phase Is Separate From Phase 2

Phase 2 built the skeleton and UI elements. This phase builds the actual content blocks that render data from the JSON. These components need real (or realistic) data to develop against, which is why Phase 3 runs in parallel.

### Build Order (Recommended)

Build blocks in order of simplicity and dependency. Each block should be testable immediately after creation using the DUI Florida data.

**4A: BlufCallout**

The simplest block. Renders a BLUF (Bottom Line Up Front) statement in a prominent callout box. Content comes from the Markdown body or a referenced content snippet. No data integration -- just styled text.

**4B: FAQBlock**

Renders the FAQ array from the JSON. Also generates the FAQPage JSON-LD schema entry. This is the first block that reads from the data JSON, so it validates that the data pipeline works end to end.

**Test:** FAQ renders on page. Schema appears in page source. Test schema against Rich Results Test.

**4C: SentencingReality**

The first complex data block. Renders the county table with jail rates, classifications, and interpretation. Implements the three presentation templates (booking artifact, real jail, mixed) driven by the `jailClassification` field. Handles display tier logic (full vs. limited vs. suppressed).

This is the block that proves the entire data-to-rendering pipeline works. If this block renders correctly for all 67 counties with appropriate classifications, caveats, and suppression -- the architecture is validated.

**4D: FinancialBurden**

Table showing county-level financial data. Simpler than SentencingReality (no classification logic) but introduces range display and handling of counties with null financial data.

**4E: NonConvictionPathways**

Table or callout showing diversion, dismissal, and AW rates per county. Highlights high-variance counties (Orange at 40.9% vs. Collier at 0.7%).

**4F: ComparisonHighlight**

The Duval vs. Pinellas proof case component. Renders the pre-built comparison narrative from the JSON's `comparisons` object. Two-column layout with interpretation text.

This component is editorially important -- it's the clearest demonstration of why the site exists. Spend extra time on the design. It should be visually distinct and immediately comprehensible.

**4G: CountyWidget (Interactive)**

The dropdown-based county selector. This is the one component with client-side JavaScript. Build it as described in the architecture report (Section 6). All county cards pre-rendered at build time; JS only handles show/hide.

**Test thoroughly:** Verify every county renders correctly, including suppressed counties (Miami-Dade), limited-data counties, and counties with caveats. Verify the dropdown works on mobile.

**4H: CoOccurringCharges**

Compact list of top co-occurring charges with counts/percentages. Relatively simple.

**4I: StatutoryOverview**

Static content block for the statutory penalty structure. Minimal data integration -- mostly editorial content with statutory references.

**4J: MethodologyInline**

Renders an inline methodology note that links to the full methodology page. Can be auto-generated from the JSON's `decisionLog` field for data-specific methodology, or reference manually written methodology for editorial methodology.

**4K: AWExplanation (For Future Charge Types)**

Block explaining Adjudication Withheld. Not needed for DUI (2.1% AW) but critical for Battery (21.2%), Drug Possession (20.1%), and most other charge types. Build it now or defer to when Battery is built -- either works since it's independent of other blocks.

### After All Blocks Are Built

Create a test page that uses every block in sequence, pointed at the DUI Florida data. Review the full page rendering. Check:

- Do all numbers match your source spreadsheet?
- Do all classification-driven templates render correctly?
- Do suppressed counties show suppression messages, not blank space?
- Do caveats display where expected?
- Is the county widget functional on mobile?
- Does the page load in under 100ms locally?

### Output

A complete set of functional content blocks, each independently testable, all rendering real DUI Florida data correctly.


---

## Phase 5: Schema / JSON-LD Integration

### 5A: Build Schema Generator Script

Write a build-time script that reads the data JSON and produces JSON-LD schema. This script runs during the Astro build process and injects schema into the page's `<head>`.

**Schema types to generate:**
- `Article` -- from page frontmatter (title, date, description)
- `Dataset` -- from `meta` and `statewide` objects in data JSON
- `FAQPage` -- from `faq` array in data JSON
- `ClaimReview` -- from `comparisons` object (if the comparison makes a specific factual claim)

### 5B: Test Generated Schema

After the DUI Florida charge page is fully assembled with real data and auto-generated schema:

1. Build the site: `npm run build`
2. Open the generated HTML file from the `/dist` folder
3. Copy the JSON-LD block from the `<head>`
4. Test against Rich Results Test and Schema.org validator
5. Fix any errors

**This validates the Phase 0 result with real data.** Phase 0 tested with a hand-built schema. This tests with the auto-generated version.

### 5C: Build Validation Page (Development Tool)

Create a non-public page (`/dev/validation`) that renders a two-column comparison for every data point: "JSON value | Rendered value." This is your check-your-work tool. Run it after every data refresh to confirm no misalignment between source data and rendered output.

### Output

Auto-generated, validated JSON-LD schema on every page. A validation tool for confirming data accuracy.


---

## Phase 6: First Complete Page -- DUI Florida

### Why This Is Its Own Phase

Everything before this was building infrastructure. This phase assembles the first real, publishable page. It's the proof of concept for the entire platform.

### 6A: Write the DUI Florida Content

Using the DUI page architecture document as the guide, write the editorial content for each block. This is writing, not coding. The frontmatter block list determines structure; the Markdown body and component content provide the editorial interpretation.

Key content to write:
- BLUF statement (the first thing the reader sees)
- Interpretation text for the SentencingReality block's intro
- Comparison narrative for the Duval/Pinellas proof case (may already be drafted in working notes)
- FAQ answers (data-grounded, reader-benefit-focused)
- Methodology notes (what data this uses, what it covers, what it doesn't)

**Reader model to hold in mind while writing:** A person charged with DUI in Florida, at 2 AM, on their phone, scared. BLUF first, jail reality second, financial reality third, can this be beaten fourth, my specific county fifth.

### 6B: Assemble the Page

Create `dui-florida.md` with:
- Frontmatter: layout, metadata, block list in reader-priority order
- Body: any additional editorial content not handled by blocks

### 6C: Write the Methodology Page

This page describes:
- What CJDT data is and where it comes from
- How you filter for DUI (statute 316.193, exclusions)
- The jail classification methodology (thresholds, criteria)
- The confidence tier system
- What the data does and does not cover
- Miami-Dade and Broward disclosure
- Temporal window rationale

**Critical:** Each decision should be an individually anchor-linked section (e.g., `/methodology/#jail-classification-criteria`). Inline methodology notes on the charge page will deep-link to specific sections, not just to "the methodology page" generically. Each decision section is a potential `ClaimReview` entry -- a falsifiable methodological claim. See architecture report Section 9.

This is one of the highest-value pages on the site. Write it with the same care as the charge page.

### 6D: Write the About / Data Catalog Page

Credibility signals. Who is behind this data. Why this approach exists. What makes it different from existing resources. Keep it concise and factual.

If implementing a `DataCatalog` schema (see architecture report Section 7), this page (or the homepage) is where it lives -- a machine-readable index of all available datasets.

### 6E: Set Up Public Data Endpoint

Copy `dui-florida.json` to `/public/data/dui-florida.json`. Add a `README.md` at `/public/data/` explaining the data structure and how to interpret confidence tiers. This is first-class citation infrastructure (architecture report Section 8), not an afterthought. It should go live with the first page.

### 6F: Full Review

View the complete DUI Florida page at `localhost:4321`:
- Read it as if you're the 2 AM reader. Does it answer your questions in order?
- Check every number against your source data
- Check schema in page source (verify `ClaimReview` entries are present and correct)
- Test on mobile (browser dev tools or actual phone)
- Test county widget with 5+ counties across all display tiers
- Verify the default-visible statewide summary card renders without interaction
- Run Lighthouse audit
- Check page load time
- **Verify internal links:** methodology page links back to charge page. Charge page inline caveats link to specific methodology anchors. No broken internal links.
- **Verify public data endpoint:** `/data/dui-florida.json` is accessible and valid JSON

### 6G: Deploy

Push to Git. Verify auto-build succeeds. View live page on Cloudflare/Netlify URL. Run Rich Results Test against the live URL.

### Output

One fully functional, editorially complete, data-backed, schema-rich charge page live on the internet. This is the proof case for the entire platform thesis.


---

## Phase 7: Expand Within DUI

### 7A: Situational Pages

Build 1-2 situational pages using the `SituationalPage.astro` layout:
- **First DUI Florida** -- uses the MDM_PERSON_ID methodology for first-offense identification. Same data JSON (filtered view), different editorial framing.
- **DUI Refusal Florida** -- uses the 316.1939 data. May need a supplementary JSON or a section within the DUI JSON.

These pages test whether the block assembly system handles different page types with different block compositions from the same data source.

### 7B: Statute/Infrastructure Pages (If Applicable)

Tier 1 pages (316.193 statute explanation, related statutes) if the content architecture calls for them. These are simpler pages -- mostly editorial content with statutory references, minimal data integration.

### Output

A small cluster of DUI pages demonstrating that the platform handles hub pages, situational pages, and infrastructure pages from the same data and component system.


---

## Phase 8: Second Charge Type -- Battery

### Why This Phase Matters

Battery validates that the pipeline generalizes. If the same components, layouts, and data architecture work for a charge type with a fundamentally different editorial story (AW-driven instead of sentencing-driven), the framework is confirmed.

### 8A: Battery Data Analysis

Apply the same analytical pipeline to battery data:
- Filter CJDT for battery statutes
- Profile disposition (expect ~21% AW, ~18% diversion -- radically different from DUI)
- Identify the editorial story (likely: DV indicator split, high AW rate, diversion variance)
- Classify counties on whatever metric is battery's equivalent of the jail booking artifact
- Produce verified numbers

### 8B: Create battery-florida.json

Same structural conventions as the DUI JSON, but with battery-specific fields:
- DV indicator data (if the DV field validates)
- AW rate prominence (this becomes a primary metric, not a footnote)
- Diversion program data
- Battery-specific caveats

### 8C: Build Battery-Specific Blocks (If Needed)

Likely new blocks:
- `DVSplit.astro` -- two-column comparison of DV vs. non-DV battery outcomes
- `AWExplanation.astro` -- if not already built in Phase 4

Existing blocks (SentencingReality, FinancialBurden, CountyWidget, etc.) should work with battery data if the JSON structure follows conventions.

### 8D: Assemble and Review

Create `battery-florida.md` with battery's block composition. Different blocks, different order, same system. Review as in Phase 6E.

### Output

Second charge type live, confirming the framework generalizes. Any needed adjustments to the block library or JSON conventions are documented.


---

## Phase 9: Ongoing Operations

### What Routine Work Looks Like

**Content edits (anytime):**
Edit Markdown files. Push to Git (or publish via Decap CMS). Auto-deploys.

**Data refresh (every 6-12 months):**
1. Download updated CJDT data
2. Re-apply your documented analytical pipeline (thresholds, filters, classifications)
3. Produce updated numbers
4. Convert to JSON, replacing existing files in `/src/data/`
5. Run validation script to catch any structural issues
6. Review rendered pages (use the validation page from Phase 5C)
7. Push to Git. Auto-deploys.

**Adding a new charge type:**
1. Run analytical pipeline on new charge type data
2. Create JSON file following established conventions
3. Build any charge-type-specific blocks needed
4. Register new blocks in ChargePage layout
5. Create Markdown page with appropriate block assembly
6. Review and deploy

**Adding a situational page:**
1. Create new Markdown file with appropriate layout and block list
2. Point to existing data JSON (or create supplementary JSON if needed)
3. Write editorial content
4. Deploy

### What Breaks and How To Fix It

| Symptom | Likely Cause | Fix |
|---|---|---|
| Build fails after JSON edit | Schema validation caught a structural error | Read the error message -- it will identify the field and file. Fix the JSON. |
| Page renders but shows "undefined" | Field name mismatch between JSON and component | Check the field names in the JSON against what the component expects. Usually a typo. |
| Page looks wrong on mobile | CSS issue | Check responsive styles. LLM can debug from a screenshot. |
| Deploy doesn't trigger after push | Git push didn't reach GitHub | Verify with `git status` and `git log`. Usually a network issue. Push again. |
| Schema test fails on live page | Schema structure issue | Extract JSON-LD from page source, test in validator, fix the schema generator. |

---

## Dependency Map (What Blocks What)

```
Phase 0: Schema Density Test -----> Phase 3A: Data Analysis (START IMMEDIATELY)
  |                                   |  (no technical dependencies --
  | (Must pass before                 |   cleaning, verifying, computing
  |  Phase 2 begins)                  |   happens in spreadsheets/notebooks)
  v                                   |
Phase 1: Environment Setup           |
  |                                   |
  v                                   |
Phase 2: Project Scaffolding          |
  |        \                          |
  v         v                         v
Phase 3B-D: Phase 4:            Phase 3A output
JSON + Val  Content Blocks      (verified numbers)
  |         /                   feeds into 3B
  v        v
Phase 5: Schema Integration
  |
  v
Phase 6: First Complete Page (DUI Florida)
  |
  v
Phase 7: Expand Within DUI
  |
  v
Phase 8: Second Charge Type (Battery)
  |
  v
Phase 9: Ongoing Operations
```

**Parallel work opportunities:**
- **Phase 3A (data analysis) starts immediately** -- it is the project bottleneck and has zero dependency on any technical setup. Every day of verified data earlier is a day the proof-of-concept page ships sooner.
- Phase 3B-D (JSON creation, schema contract, validation script) need Phase 2's scaffolding to test against, but the analytical work feeding them should already be underway.
- Content writing (editorial) can happen anytime -- it's independent of technical build.
- Domain registration and DNS setup can happen anytime during or after Phase 1.

---

## LLM Implementation Notes

**For any LLM helping with the technical build:**

1. **Read the technical architecture report first.** It contains the full reasoning for every structural decision. Don't override those decisions without discussing with the project owner.

2. **The block assembly system is the core mechanism.** If you're unsure how to implement something, ask: "Does this fit as a block component that's registered in the layout and referenced in frontmatter?" Usually the answer is yes.

3. **The JSON is the single source of truth for all data.** Components should never contain hardcoded numbers. Every data point comes from the JSON. If a number needs to change, it changes in the JSON -- never in a component.

4. **The project owner prefers minimal troubleshooting.** When generating code, favor simple, readable implementations over clever ones. Explicit is better than implicit. A few extra lines of clear code are better than a one-liner that's hard to debug.

5. **Test incrementally.** Don't build five components and then test. Build one, test it, confirm it works, move to the next. The project owner needs to see progress and catch issues early.

6. **Respect the content architecture.** The V5 checkpoint, working notes, and page architecture documents govern WHAT goes on pages and WHY. This build sequence and the technical architecture report govern HOW it gets built. Don't let technical convenience override editorial decisions.

7. **The site is designed to be extracted from.** Semantic HTML, proper heading hierarchy, no JavaScript-gated content. If you're tempted to add a "click to expand" or lazy-load pattern, don't -- it conflicts with the LLM extraction optimization strategy.

8. **Static is the point.** If you find yourself reaching for a server-side solution, API endpoint, or dynamic data fetch, stop and reconsider. The entire architecture is built around the principle that all computation happens before the site is built. The site renders pre-computed results. If you need something dynamic, the county widget is the one exception -- everything else is static HTML.

---

## Document Metadata

- **Supplements:** technical-architecture-report.md, project-handoff-report.md
- **Status:** Pre-build planning. Will be updated as phases are completed.
- **Sequencing logic:** Each phase produces a testable artifact. Blockers are identified. Parallel opportunities are noted. The owner can stop at any phase boundary and have a functional (if incomplete) product.
