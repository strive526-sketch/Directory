# Technical Architecture Report -- Legal Data Synthesis Platform

**Date:** March 20, 2026
**Status:** Draft v1.2 -- Revised with citation authority optimization
**Purpose:** Technical reference for site architecture, stack decisions, data flow, and component design. Written for the project owner and any LLM assisting with implementation.

---

## How To Use This Document

This is the technical grounding document. It covers what we're building, why each decision was made given the project owner's constraints, and how the pieces connect. Code examples are illustrative, not final -- they represent the intended approach and will iterate during development.

**This document does NOT replace the project's content architecture documents** (V5, working notes, DUI page architecture, charge page framework). Those govern what goes on each page and why. This document governs how those pages get built and served.

---

## 1. Architecture Overview

### What We're Building

A static content site with pre-computed data integration and one interactive element per charge page. Content lives in Markdown. Data lives in JSON. Components render both into static HTML at build time. The output is flat HTML files served from a CDN.

### The Core Technical Principle

The website does not compute anything. Every number, every percentage, every classification, every caveat -- all of it is determined before it reaches the site. The site is a rendering layer, not an analytical layer. This is a deliberate architectural choice driven by:

1. **Reliability** -- static files on a CDN have near-zero failure modes in production
2. **Performance** -- no server, no database queries, no runtime. HTML on edge nodes. Sub-100ms loads.
3. **Maintainability** -- the project owner is not a developer. Ongoing work should be editing Markdown and replacing JSON files, not debugging server processes.
4. **Correctness** -- every number is verified before it enters the site. There is no query logic in the rendering layer that could silently compute wrong results.

### High-Level Data Flow

```
[Your analytical work]
  Spreadsheets, LLM assistance, manual verification
  All cleaning, calculating, classifying happens here
      |
      v
[Pre-computed JSON files]
  One per charge type (dui-florida.json, battery-florida.json, etc.)
  Contains every number, classification, confidence tier, caveat
  This is the handoff artifact -- the bridge between analysis and site
      |
      v
[Astro static site generator]
  Reads JSON + Markdown at BUILD time (not at request time)
  Assembles pages from modular components based on frontmatter config
  Outputs pure HTML + minimal JS (county widget only)
      |
      v
[CDN (Cloudflare Pages or Netlify)]
  Hosts static HTML files globally
  Auto-builds on Git push
  No server to manage, no database to maintain
```

---

## 2. Stack Selection and Reasoning

### Astro (Site Generator)

**Why Astro over alternatives:**

| Consideration | Astro | WordPress | Next.js | Plain HTML |
|---|---|---|---|---|
| Production failure surface | Near-zero (static files) | High (PHP, MySQL, plugins, caching) | Medium (Node server, hydration) | Near-zero |
| Ongoing maintenance | Markdown + JSON edits | Plugin updates, security patches, DB backups | Dependency management, server monitoring | Manual HTML edits across all pages |
| Component reuse | Native (`.astro` components) | Requires theme/plugin dev | Native but over-engineered | None (copy-paste) |
| Performance | Static HTML on CDN | Requires caching layer to compete | SSG mode matches, SSR mode slower | Static HTML on CDN |
| LLM-assisted editing | Excellent (Markdown is native) | Moderate (DB-backed content) | Good but complex codebase | Good but repetitive |
| Interactive elements | Islands architecture (JS only where needed) | Plugin-dependent | Full React (ships too much JS) | Manual JS integration |
| Shared layouts | Built-in | Theme system | Built-in | None |
| JSON-LD injection | Direct control in layouts | Plugin-mediated, limited | Direct control | Direct control |
| Learning curve for owner | Low (Markdown + YAML frontmatter) | Known but wrong tool | High (React ecosystem) | Lowest but unscalable |

**The decisive factors for this project specifically:**

1. Astro's output is plain HTML. If something works in `npm run dev`, it works in production. There is no gap between preview and live.
2. The "islands" model means the county interactive widget ships JavaScript; everything else ships zero JS. Minimal client-side complexity.
3. `.astro` files look like HTML with a data section at the top. They are not React components. The syntax is approachable for someone comfortable with basic HTML.
4. Astro has extensive LLM training data coverage. Claude, GPT-4, etc. can generate and debug Astro code reliably.

### Cloudflare Pages (Hosting / CDN)

**Why Cloudflare Pages:**

- Free tier handles this project's scale comfortably (unlimited bandwidth, 500 builds/month)
- Global CDN with edge caching -- matches or beats FCF's 0.07s loads
- Auto-builds from Git push -- no manual deploy step
- No server to manage, no containers, no infrastructure
- Custom domain support with free SSL

**Alternative:** Netlify is functionally equivalent. Either works. Cloudflare's edge network is slightly larger. Netlify's UI is slightly more intuitive. Marginal difference. Pick one and commit.

### Git / GitHub (Version Control + Deployment Trigger)

Git is the deployment mechanism for both Cloudflare Pages and Netlify. Pushing to the repository triggers an automatic rebuild and deploy. The workflow:

```
Edit file locally (or via visual editor)
  -> git add . && git commit -m "message" && git push
    -> Cloudflare detects push, runs Astro build
      -> New static files deployed to CDN globally
```

**For the project owner's comfort level:** GitHub Desktop provides a visual interface. The operations are: review changes, write a commit message, click "Commit", click "Push." No terminal required for routine work.

**Optional: Decap CMS (Visual Editor Layer)**

Decap CMS (formerly Netlify CMS) provides a browser-based editing interface on top of the Git repository. After one-time configuration, the workflow becomes:

```
Log into yoursite.com/admin
  -> See list of pages
    -> Click a page to edit
      -> Edit Markdown in visual editor
        -> Click "Publish"
          -> Decap commits to Git behind the scenes
            -> Auto-build triggers
```

This completely hides Git from the content editing workflow. It does NOT handle the frontmatter block assembly (choosing which components in which order) -- that's still a YAML edit. But for content text changes, it's browser-based.

**Decision needed:** Whether to include Decap CMS in the initial build. It adds ~2 hours to setup and one config file. Recommendation: include it. The marginal setup cost is low and it removes friction from the most common task (editing page content).

---

## 3. Project Structure

```
/legal-data-platform/
|
|-- /src/
|   |-- /content/              <-- Your page files (Markdown)
|   |   |-- dui-florida.md
|   |   |-- dui-florida-first-offense.md
|   |   |-- dui-florida-refusal.md
|   |   |-- battery-florida.md
|   |   |-- methodology.md
|   |   |-- about.md
|   |
|   |-- /layouts/              <-- Page templates (written once)
|   |   |-- ChargePage.astro        <-- Main layout for charge type pages
|   |   |-- SituationalPage.astro   <-- Layout for first-offense, refusal, etc.
|   |   |-- StaticPage.astro        <-- Layout for methodology, about, etc.
|   |   |-- BaseLayout.astro        <-- Shared HTML head, nav, footer
|   |
|   |-- /components/           <-- Modular content blocks (the block library)
|   |   |-- blocks/
|   |   |   |-- BlufCallout.astro
|   |   |   |-- SentencingReality.astro
|   |   |   |-- FinancialBurden.astro
|   |   |   |-- NonConvictionPathways.astro
|   |   |   |-- AWExplanation.astro
|   |   |   |-- CountyWidget.astro       <-- Interactive (ships JS)
|   |   |   |-- CoOccurringCharges.astro
|   |   |   |-- StatutoryOverview.astro
|   |   |   |-- CircumstanceModifier.astro
|   |   |   |-- ProceduralNextSteps.astro
|   |   |   |-- AttorneyContext.astro
|   |   |   |-- FAQBlock.astro
|   |   |   |-- MethodologyInline.astro
|   |   |   |-- ComparisonHighlight.astro  <-- Duval/Pinellas style proof case
|   |   |
|   |   |-- ui/               <-- Reusable styled elements
|   |   |   |-- CalloutBox.astro
|   |   |   |-- DataTable.astro
|   |   |   |-- InterpretationNote.astro
|   |   |   |-- CaveatBanner.astro
|   |   |   |-- ConfidenceBadge.astro
|   |   |   |-- SourceCitation.astro
|   |   |
|   |   |-- layout/           <-- Structural elements
|   |       |-- Navigation.astro
|   |       |-- Footer.astro
|   |       |-- SchemaInjector.astro
|   |       |-- SEOHead.astro
|   |
|   |-- /data/                 <-- Pre-computed JSON files
|   |   |-- dui-florida.json
|   |   |-- battery-florida.json
|   |   |-- schemas/                <-- Generated JSON-LD (build-time)
|   |       |-- dui-florida-schema.json
|   |
|   |-- /schemas/              <-- JSON schema contracts (validation)
|   |   |-- charge-type.schema.json
|   |   |-- county-data.schema.json
|   |
|   |-- /styles/               <-- Global CSS
|       |-- global.css
|       |-- variables.css
|
|-- /public/                   <-- Static assets (images, favicons)
|   |-- /data/                 <-- Public data endpoint (see Opportunity 4)
|       |-- dui-florida.json   <-- Copy of data JSON, publicly accessible
|
|-- /scripts/                  <-- Build-time utilities
|   |-- validate-data.js       <-- Checks JSON against schema contracts
|   |-- generate-schemas.js    <-- Produces JSON-LD from data JSONs
|
|-- astro.config.mjs           <-- Astro configuration
|-- package.json
|-- README.md
```

### Where Things Live -- Quick Reference

| What you're doing | Where the file is |
|---|---|
| Writing/editing page content | `/src/content/*.md` |
| Updating data for a charge type | `/src/data/*.json` |
| Changing shared page structure (nav, footer) | `/src/layouts/` and `/src/components/layout/` |
| Changing how a data block looks | `/src/components/blocks/` |
| Changing a styled element (callout box, table) | `/src/components/ui/` |
| Adding a new charge type | New `.md` in content + new `.json` in data |
| Adding a new block type | New `.astro` in components/blocks + register in layout |

---

## 4. The Block Assembly System

This is the core mechanism that allows mix-and-match page composition without code changes.

### How It Works

Each page's Markdown file has a `blocks` list in its frontmatter. The layout reads this list and renders the corresponding component for each entry, in order, passing it the page's data.

### Page Example: DUI Florida (Charge Hub Page)

```markdown
---
layout: ../layouts/ChargePage.astro
title: "DUI in Florida -- What Actually Happens (2023-2025 Court Data)"
charge: "dui"
state: "florida"
statute: "316.193"
dataFile: "dui-florida.json"
schemaFile: "dui-florida-schema.json"
dataWindow: "2023-2025"
dataSource: "FDLE CJDT Clerk Case Data"
seoDescription: "Florida DUI outcomes based on 62,558 court cases. County-level conviction rates, actual jail time, financial costs, and non-conviction pathways."

blocks:
  - type: "bluf"
    style: "callout-primary"
    content: "bluf-dui-florida"
  - type: "sentencing-reality"
    style: "table-with-interpretation"
    showClassification: true
  - type: "comparison-highlight"
    counties: ["duval", "pinellas"]
    narrative: "comparison-duval-pinellas"
  - type: "financial-burden"
    style: "range-table"
    showStatewide: true
  - type: "non-conviction-pathways"
    style: "callout-with-table"
  - type: "county-widget"
    style: "dropdown-card"
  - type: "co-occurring"
    style: "compact-list"
    limit: 5
  - type: "faq"
    content: "faq-dui-florida"
  - type: "methodology-inline"
    scope: "page"
---

[Optional additional Markdown content that appears after the assembled blocks.
This is where editorial narrative, context, or supplementary text goes.
Most structured content is handled by the blocks above.]
```

### Page Example: Battery Florida (Different Block Order, Different Blocks)

```markdown
---
layout: ../layouts/ChargePage.astro
title: "Battery in Florida -- Court Outcomes and What They Mean (2023-2025)"
charge: "battery"
state: "florida"
statute: "784.03"
dataFile: "battery-florida.json"
dataWindow: "2023-2025"

blocks:
  - type: "bluf"
    style: "callout-primary"
    content: "bluf-battery-florida"
  - type: "aw-explanation"
    style: "callout-highlight"
  - type: "dv-split"
    style: "two-column-comparison"
  - type: "non-conviction-pathways"
    style: "table-with-interpretation"
  - type: "sentencing-reality"
    style: "table-with-interpretation"
  - type: "county-widget"
    style: "dropdown-card"
  - type: "co-occurring"
    style: "compact-list"
  - type: "faq"
    content: "faq-battery-florida"
---
```

Note: different blocks (aw-explanation, dv-split are present; comparison-highlight is absent), different order (AW and DV are prioritized over sentencing for battery). Same system, same layout, different assembly.

### The Layout That Makes This Work

The `ChargePage.astro` layout reads the frontmatter `blocks` array and renders each component. Simplified illustration:

```astro
---
// ChargePage.astro
import BaseLayout from './BaseLayout.astro';
import BlufCallout from '../components/blocks/BlufCallout.astro';
import SentencingReality from '../components/blocks/SentencingReality.astro';
import FinancialBurden from '../components/blocks/FinancialBurden.astro';
import NonConvictionPathways from '../components/blocks/NonConvictionPathways.astro';
import AWExplanation from '../components/blocks/AWExplanation.astro';
import CountyWidget from '../components/blocks/CountyWidget.astro';
import ComparisonHighlight from '../components/blocks/ComparisonHighlight.astro';
import CoOccurringCharges from '../components/blocks/CoOccurringCharges.astro';
import FAQBlock from '../components/blocks/FAQBlock.astro';
import MethodologyInline from '../components/blocks/MethodologyInline.astro';
import DVSplit from '../components/blocks/DVSplit.astro';

const { frontmatter } = Astro.props;
const data = await import(`../data/${frontmatter.dataFile}`);

// Component registry -- maps block type strings to actual components
const blockRegistry = {
  'bluf': BlufCallout,
  'sentencing-reality': SentencingReality,
  'financial-burden': FinancialBurden,
  'non-conviction-pathways': NonConvictionPathways,
  'aw-explanation': AWExplanation,
  'county-widget': CountyWidget,
  'comparison-highlight': ComparisonHighlight,
  'co-occurring': CoOccurringCharges,
  'faq': FAQBlock,
  'methodology-inline': MethodologyInline,
  'dv-split': DVSplit,
};
---

<BaseLayout title={frontmatter.title} schema={frontmatter.schemaFile}>
  <article>
    <h1>{frontmatter.title}</h1>

    {frontmatter.blocks.map((block) => {
      const Component = blockRegistry[block.type];
      if (!Component) return null;
      return <Component data={data} config={block} />;
    })}

    <!-- Any additional Markdown content from the page body -->
    <slot />
  </article>
</BaseLayout>
```

### Adding a New Block Type

When a new charge type needs a block that doesn't exist yet (e.g., battery needs `DVSplit`):

1. Create `/src/components/blocks/DVSplit.astro`
2. Design and style the component
3. Add one line to the `blockRegistry` in ChargePage.astro: `'dv-split': DVSplit`
4. Reference it in any page's frontmatter `blocks` list

That's the full process. The layout doesn't change structurally; it just gains awareness of a new block type.

---

## 5. Data Architecture

### The JSON Contract

Each charge type produces one JSON file containing every pre-computed number the site will display. The structure adapts per charge type -- DUI's JSON focuses on jail classification and sentencing; Battery's would focus on DV splits and AW rates. The structure does not need to be identical across charge types, but should follow consistent conventions.

### Illustrative JSON Structure (DUI Florida)

```json
{
  "meta": {
    "charge": "dui",
    "state": "florida",
    "statute": "316.193",
    "dataWindow": "2023-2025",
    "dataSource": "FDLE CJDT Clerk Case Data",
    "lastUpdated": "2026-03-15",
    "totalCases": 62558,
    "decisionLog": {
      "jailClassificationCriteria": "Booking Artifact if >=50% sentences 1-2 days AND >=70% CTS coverage",
      "exclusions": "316.1935 and 316.1939 excluded from primary DUI filter",
      "miamiDade": "Excluded from statewide calculations due to data submission gap (167 records for 2.7M population)",
      "trailingWindow": "2023-2025 selected for comparability with FCF and data stability post-onboarding",
      "lowVolumeThreshold": ">=50 jail cases for full classification, 10-49 for rate with caveat, <10 suppressed"
    }
  },

  "statewide": {
    "convictionRate": 93.4,
    "awRate": 2.1,
    "diversionRate": 1.6,
    "dismissalRate": 1.7,
    "medianFinancialBurden": 1468,
    "financialRange": { "low": 931, "high": 2912 },
    "sampleSize": 62558,
    "confidence": "high",
    "caveats": ["miami-dade-excluded"]
  },

  "counties": {
    "duval": {
      "name": "Duval",
      "population": 1018000,
      "totalConvictions": 3842,
      "jailRate": 86.0,
      "jailClassification": "booking-artifact",
      "jailMetrics": {
        "medianSentenceDays": 2,
        "pct1to2Day": 58.6,
        "ctsCoverage": 85.6,
        "pct31PlusDays": 8.2
      },
      "financial": {
        "medianTotal": 1623,
        "fineMedian": 987,
        "courtCostMedian": 636,
        "coverage": 82.3
      },
      "nonConviction": {
        "totalRate": 8.2,
        "diversionRate": 1.1,
        "dismissalRate": 3.4,
        "awRate": 1.8
      },
      "sampleSize": 3842,
      "confidence": "high",
      "displayTier": "full",
      "caveats": []
    },

    "miami-dade": {
      "name": "Miami-Dade",
      "population": 2700000,
      "totalConvictions": 167,
      "jailRate": null,
      "jailClassification": null,
      "financial": null,
      "nonConviction": null,
      "sampleSize": 167,
      "confidence": "low",
      "displayTier": "suppressed",
      "caveats": ["data-submission-gap"],
      "suppressionReason": "Only 167 DUI dispositions reported 2023-2025 for a county of 2.7 million. Data appears substantially incomplete."
    }
  },

  "comparisons": {
    "duval-pinellas": {
      "title": "Why 86% Jail Can Be Less Severe Than 42%",
      "countyA": "duval",
      "countyB": "pinellas",
      "narrative": "Duval's 86% jail rate is dominated by 1-2 day booking credits (58.6% of jail sentences). In 85.6% of cases, time already served at arrest covers the entire sentence. Pinellas at 42% has a median sentence of 60 days with only 29% covered by credit time served. The reader comparing raw percentages would conclude Duval is far harsher. The reality is inverted.",
      "implication": "Raw jail percentages without sentence length and credit time served context can produce the opposite conclusion from reality."
    }
  },

  "faq": [
    {
      "question": "How likely am I to go to jail for a DUI in Florida?",
      "answer": "It depends heavily on your county. The statewide conviction rate is 93.4%, but what 'jail' means varies. In some counties (like Duval and Orange), the majority of recorded jail sentences are 1-2 day booking credits from the night of arrest -- not additional jail time after court. In other counties (like Pinellas and Pasco), jail sentences average 60-90 days of real post-conviction incarceration. Based on 62,558 DUI convictions, 2023-2025, FDLE CJDT data.",
      "dataPoints": ["statewide.convictionRate", "counties.duval.jailClassification", "counties.pinellas.jailMetrics.medianSentenceDays"]
    }
  ]
}
```

### Key Design Decisions in the JSON

**1. The `decisionLog` field:** Embeds your analytical methodology directly in the data file. When you refresh data in 12 months, this tells you (and any LLM helping you) exactly what criteria were applied. It also means the methodology is version-controlled -- if you change a threshold, the change is tracked in Git alongside the data it affects.

**2. The `displayTier` field:** Drives component rendering logic. Values: `"full"` (show everything), `"limited"` (show rate with caveat), `"suppressed"` (show only suppression message). Components check this field and render accordingly. You don't write conditional logic per county -- you encode the decision in the data.

**3. The `caveats` array:** Standardized caveat codes that map to specific disclosure text in components. `"data-submission-gap"`, `"low-sample-size"`, `"sentinel-value-contamination"`, `"booking-artifact-mixed"`, etc. The component looks up the code and renders the appropriate caveat language. Adding a new caveat type means adding one code-to-text mapping.

**4. The `comparisons` object:** Pre-built comparison narratives for the ComparisonHighlight block. The editorial interpretation is in the JSON, not in the component code. The component just renders it. This means comparison text is editable without touching any code.

**5. The `faq` array:** FAQ content lives in the data file so it can be charge-type-specific and data-referenced. The FAQBlock component renders it and the SchemaInjector produces FAQPage schema from it automatically.

### Schema Contract Validation

**Why this matters:** If a field name is misspelled in the JSON or a required field is missing, the component will silently render nothing (or render "undefined"). With pre-computed data and infrequent updates, this error could persist for months.

**Solution:** A JSON Schema file defines the required structure. A build-time validation script checks every data JSON against its schema contract before the build proceeds. If validation fails, the build aborts with a clear error message identifying exactly which field is wrong.

```json
// /src/schemas/charge-type.schema.json (simplified)
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["meta", "statewide", "counties"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["charge", "state", "dataWindow", "lastUpdated", "totalCases"]
    },
    "statewide": {
      "type": "object",
      "required": ["convictionRate", "sampleSize", "confidence"]
    },
    "counties": {
      "type": "object",
      "patternProperties": {
        ".*": {
          "type": "object",
          "required": ["name", "totalConvictions", "sampleSize", "confidence", "displayTier"]
        }
      }
    }
  }
}
```

The validation script runs as part of the build process. If you push a JSON file with a missing `sampleSize` field, the build fails immediately and tells you which county is missing which field.

---

## 6. Component Design

### Block Components

Each block component follows the same pattern: receive data + config, check display conditions, render appropriate template variant.

### Illustrative Component: SentencingReality

```astro
---
// SentencingReality.astro
// Renders jail rate data with interpretation based on county classification

const { data, config } = Astro.props;
const counties = Object.values(data.counties)
  .filter(c => c.displayTier !== 'suppressed' && c.jailRate !== null)
  .sort((a, b) => b.totalConvictions - a.totalConvictions);

const classificationLabels = {
  'booking-artifact': 'Mostly booking credit',
  'real-jail': 'Real post-conviction jail',
  'mixed': 'Mixed pattern'
};
---

<section class="block sentencing-reality" aria-label="Sentencing outcomes by county">
  <h2>What "Jail" Actually Means in Your County</h2>

  <div class="interpretation-note">
    <p>Florida DUI jail rates range from 4% to 88% depending on the county.
    But these numbers can be misleading. In some counties, the recorded "jail sentence"
    is a 1-2 day booking credit from the night of arrest -- the defendant does not
    return to custody. In other counties, it means 30-90 days of real incarceration.</p>
    <p class="source-citation">Based on {data.meta.totalCases.toLocaleString()} DUI
    convictions, {data.meta.dataWindow}, {data.meta.dataSource}.</p>
  </div>

  {config.showClassification && (
    <table class="data-table">
      <thead>
        <tr>
          <th>County</th>
          <th>Jail Rate</th>
          <th>What It Means</th>
          <th>Median Sentence</th>
          <th>Covered by Time Served</th>
        </tr>
      </thead>
      <tbody>
        {counties.map(c => (
          <tr class={`classification-${c.jailClassification}`}>
            <td>{c.name}</td>
            <td>{c.jailRate}%</td>
            <td>
              <span class="classification-badge">{classificationLabels[c.jailClassification]}</span>
            </td>
            <td>{c.jailMetrics?.medianSentenceDays} days</td>
            <td>{c.jailMetrics?.ctsCoverage}%</td>
          </tr>
        ))}
      </tbody>
    </table>
  )}

  {counties.filter(c => c.caveats.length > 0).map(c => (
    <aside class="caveat-note">
      <strong>{c.name}:</strong> {c.caveats.map(caveat => (
        <CaveatText code={caveat} />
      ))}
    </aside>
  ))}
</section>
```

### Illustrative Component: ComparisonHighlight

This is the Duval vs Pinellas proof case -- the single most citable element on the site. It renders a pre-built comparison from the JSON's `comparisons` object.

```astro
---
// ComparisonHighlight.astro
const { data, config } = Astro.props;
const comparison = data.comparisons[`${config.counties[0]}-${config.counties[1]}`];
const countyA = data.counties[config.counties[0]];
const countyB = data.counties[config.counties[1]];
---

<section class="block comparison-highlight" aria-label="County comparison">
  <h2>{comparison.title}</h2>

  <div class="comparison-grid">
    <div class="county-card">
      <h3>{countyA.name} County</h3>
      <div class="stat-large">{countyA.jailRate}% jail rate</div>
      <div class="stat-detail">Median sentence: {countyA.jailMetrics.medianSentenceDays} days</div>
      <div class="stat-detail">Time served covers: {countyA.jailMetrics.ctsCoverage}%</div>
      <div class="classification">{countyA.jailClassification}</div>
    </div>

    <div class="comparison-arrow">vs</div>

    <div class="county-card">
      <h3>{countyB.name} County</h3>
      <div class="stat-large">{countyB.jailRate}% jail rate</div>
      <div class="stat-detail">Median sentence: {countyB.jailMetrics.medianSentenceDays} days</div>
      <div class="stat-detail">Time served covers: {countyB.jailMetrics.ctsCoverage}%</div>
      <div class="classification">{countyB.jailClassification}</div>
    </div>
  </div>

  <div class="interpretation-narrative">
    <p>{comparison.narrative}</p>
    <p class="implication"><strong>Why this matters:</strong> {comparison.implication}</p>
  </div>
</section>
```

### The County Interactive Widget

**This is the one component that ships client-side JavaScript.** Everything else is static HTML.

**Recommended initial approach:** A dropdown selector that shows/hides a pre-rendered data card per county. All county cards are built into the static HTML at build time. The JavaScript only toggles visibility -- no API calls, no dynamic data fetching.

```astro
---
// CountyWidget.astro
// All county data is pre-rendered. JS swaps visible card on selection.
// IMPORTANT: One card is visible by default (statewide summary) so crawlers
// and AI systems see county data as visible content, not display:none.
const { data, config } = Astro.props;
const counties = Object.values(data.counties)
  .sort((a, b) => a.name.localeCompare(b.name));
---

<section class="block county-widget" aria-label="County-specific data">
  <h2>Find Your County</h2>

  <select id="county-selector">
    <option value="statewide" selected>Statewide Summary</option>
    {counties.map(c => (
      <option value={c.name.toLowerCase().replace(/\s/g, '-')}>
        {c.name} County
      </option>
    ))}
  </select>

  <div id="county-cards">
    <!-- Default-visible statewide summary card -->
    <div class="county-card" id="card-statewide">
      <div class="full-data">
        <!-- Statewide summary with key metrics visible to crawlers -->
        <!-- Conviction rate, financial range, jail classification breakdown -->
        <!-- This is the content AI systems will index by default -->
      </div>
    </div>

    {counties.map(c => (
      <div class="county-card" id={`card-${c.name.toLowerCase().replace(/\s/g, '-')}`}
           style="display: none;">

        {c.displayTier === 'suppressed' ? (
          <div class="suppression-notice">
            <p>{c.suppressionReason}</p>
          </div>
        ) : c.displayTier === 'limited' ? (
          <div class="limited-data">
            <p>Based on {c.sampleSize} cases -- limited data available.</p>
            {c.jailRate && <p>Jail rate: {c.jailRate}%</p>}
          </div>
        ) : (
          <div class="full-data">
            <!-- Full county card with all metrics -->
            <!-- Classification-specific interpretation template -->
            <!-- Financial data if available -->
            <!-- Non-conviction pathway data -->
            <!-- Sample size and source citation -->
          </div>
        )}
      </div>
    ))}
  </div>
</section>

<script>
  document.getElementById('county-selector').addEventListener('change', (e) => {
    document.querySelectorAll('.county-card').forEach(card => card.style.display = 'none');
    document.getElementById(`card-${e.target.value}`).style.display = 'block';
  });
</script>
```

**Citation note on `display:none` content:** Google's indexing pipeline deprioritizes content hidden behind `display:none`. For a site whose terminal objective is citation authority, county-specific data buried behind a visibility toggle is partially invisible to the systems you're trying to be cited by. The approach above mitigates this by always rendering a statewide summary card as visible content. The full pre-rendered county table in the SentencingReality block (which IS visible) handles per-county crawlability. The widget is the interactive UX layer; the table is the citation layer.

**Upgrade paths (not for initial build):**

- **Clickable Florida map:** Replace the dropdown with an SVG map. Each county is a clickable region. Same underlying show/hide mechanism, more visual. Adds complexity (SVG paths for 67 counties) but no architectural change.
- **Side-by-side comparison:** Let the user pick two counties and see them rendered in parallel, ComparisonHighlight style. Moderate JS complexity increase.
- **Filter by classification:** Let the user filter the county list by jail classification type. Trivial JS addition to the existing dropdown.
- **Client-side rendering from inline JSON:** At 15+ charge types, the 67 pre-rendered hidden cards per page accumulate. An alternative: embed county data as an inline JSON blob and render only the selected card client-side. Same UX, less DOM weight. Not worth the complexity initially.

**Decision point:** Start with the dropdown with a default-visible statewide summary card. Visual upgrades are additive, not structural.

---

## 7. Structured Data / JSON-LD Strategy

### Why This Is Critical

The terminal objective is AI citation authority. Structured data (JSON-LD) is how search engines and LLMs understand what your page contains, how confident it is, and whether it's worth citing. This is infrastructure, not decoration.

### Schema Types Per Page Type

**Charge Page (e.g., DUI Florida):**
- `ClaimReview` -- **the primary trust signal.** The Duval/Pinellas comparison is a direct, falsifiable, verifiable factual claim with evidence. This is the schema type Google uses to evaluate factual authority for AI Overview citation eligibility. Implement with explicit `reviewRating` (True), `claimReviewed` (the raw-data interpretation that a higher jail rate means harsher sentencing), and `itemReviewed` pointing to the evidence. Every comparison in the JSON's `comparisons` object is a `ClaimReview` candidate.
- `Dataset` -- describes the underlying data (source, temporal coverage, spatial coverage, methodology)
- `Article` -- identifies the page as editorial content
- `FAQPage` -- from the FAQ block content

**Site Level (Homepage or Data Catalog Page):**
- `DataCatalog` -- describes the collection of all datasets on the platform. References each charge-type `Dataset` entry. This is how authoritative data sources (Our World in Data, etc.) signal to AI systems that they are a primary data source, not secondary commentary. One JSON-LD block that indexes the full data asset.

**Situational Page (e.g., First DUI Florida):**
- `Article`
- `FAQPage`
- Potentially `Dataset` if page-specific data is substantial

**Methodology Page:**
- `Article`
- `Dataset` (describing the CJDT source itself)

### ClaimReview Implementation

The Duval/Pinellas comparison is the single highest-citation-value element on the site. Its schema should be explicit:

```json
{
  "@type": "ClaimReview",
  "claimReviewed": "A higher county jail rate for DUI indicates harsher sentencing outcomes",
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": 1,
    "bestRating": 5,
    "alternateName": "False"
  },
  "itemReviewed": {
    "@type": "Claim",
    "author": { "@type": "Organization", "name": "Common interpretation of raw CJDT data" },
    "appearance": {
      "@type": "CreativeWork",
      "description": "Raw jail rate statistics as published on court data aggregation sites"
    }
  },
  "reviewBody": "Duval County's 86% jail rate is predominantly composed of 1-2 day booking credits (58.6% of sentences). Credit time served covers 85.6% of cases. Pinellas at 42% has a median sentence of 60 days with only 29% CTS coverage. The raw percentage inverts the actual severity ranking."
}
```

Each comparison in the JSON's `comparisons` object auto-generates a `ClaimReview`. The build-time schema generator produces these from the data, not from hand-written schema.

### Auto-Generation From Data JSON

The JSON-LD does not need to be hand-written. A build-time script reads the data JSON and produces the corresponding schema automatically. This ensures schema stays in sync with data by construction.

```javascript
// Simplified schema generation logic
function generateChargePageSchema(data) {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Article",
        "headline": `${data.meta.charge.toUpperCase()} in ${data.meta.state}`,
        "dateModified": data.meta.lastUpdated,
        // ... article metadata
      },
      {
        "@type": "Dataset",
        "name": `${data.meta.state} ${data.meta.charge.toUpperCase()} Court Outcomes`,
        "description": `Disposition and sentencing outcomes for ${data.meta.totalCases} cases`,
        "temporalCoverage": data.meta.dataWindow,
        "spatialCoverage": { "@type": "State", "name": data.meta.state },
        "measurementTechnique": data.meta.decisionLog,
        // ... dataset metadata
      },
      // ClaimReview entries from data.comparisons
      // FAQPage from data.faq array
    ]
  };
}
```

### dateModified Enforcement

The `dateModified` field in the Article schema is pulled from `lastUpdated` in the JSON meta object. On a YMYL domain in a sandbox period, a stale `dateModified` actively signals to AI evaluation systems that the data may be outdated -- undermining the authority being built during exactly the window when it matters most.

**Hard rule:** The build-time validation script (Phase 3D) must reject any JSON where `lastUpdated` is older than a configurable threshold (e.g., 14 months). This prevents deploying a site with a schema that signals staleness. The threshold is deliberately longer than the planned 6-12 month refresh cycle to allow some buffer, but short enough to catch if a refresh is forgotten.

### CRITICAL: Schema Density Testing Required Before Build

**This is flagged as a potential blocker in the project documents and it remains unresolved.**

The DUI charge page will carry a dense schema block: ClaimReview (1-3 entries) + Dataset (statewide) + potentially per-county Dataset entries + Article + FAQPage. Google's Rich Results Test has undocumented limits on schema density per page.

**Required action:** Before building any components, create a single static HTML file with the maximum schema density planned for the DUI charge page. Test against:
- Google Rich Results Test
- Schema.org validator
- Google Search Console (after deploy, for real-world validation)

**If density is a problem, fallback hierarchy:**
1. Keep ClaimReview + Article + FAQPage + statewide Dataset on the page (ClaimReview stays -- it's the primary trust signal)
2. Move per-county data to linked Dataset entries at separate URLs (e.g., `/data/dui-florida-duval.json`)
3. Limit additional Dataset entries

This test should happen before any component development begins. The result affects URL architecture.

---

## 8. Public Data Endpoint (First-Class Citation Infrastructure)

The JSON files already exist in the repo. Exposing them publicly at clean, predictable URLs is a direct RAG retrieval target -- not just a transparency gesture.

**Why this is infrastructure, not an optional add-on:** When an LLM builds a retrieval-augmented response about Florida DUI outcomes, a structured JSON endpoint with confidence tiers, caveats, and methodology embedded is exactly what a well-designed RAG pipeline prefers to retrieve over parsing HTML. The public endpoint at `yoursite.com/data/dui-florida.json` is a machine-readable citation source that serves the terminal objective directly.

**Implementation:** Copy data JSONs to `/public/data/` during the build process. They become accessible at predictable URLs. Include a `README.md` at `/public/data/` explaining the data structure and how to interpret confidence tiers.

**The `DataCatalog` schema** (Section 7) on the homepage or a dedicated `/data/` page indexes all available datasets, making the full data asset discoverable as a collection.

**Caveat:** This exposes your full data structure, including analytical decisions (classification criteria, suppression thresholds). For this project, that's a feature, not a risk -- transparency IS the credibility. But be aware that anyone (including competitors) can see exactly how you classify counties and what thresholds you use.

---

## 9. Methodology as First-Class Citable Content

The methodology page is not a footnote. It may be the single highest-citation-value page on the site.

**Why:** When an LLM is deciding whether to cite a factual claim, it evaluates the source's methodology. A page that says "we classified 42 Florida counties into three jail reporting patterns based on sentence length distribution and credit time served coverage, using these specific thresholds, validated against these cross-references" is an explicit trust signal. FCF's methodology page says "Jail = sentence of 1-365 days." The contrast is the differentiator made visible.

**Implementation:** The methodology page should carry its own rich schema (Dataset describing the CJDT source, plus Article) and should be internally linked from every data claim across the site. Inline methodology notes on charge pages should link to the relevant section of the methodology page.

### The decisionLog as Individually Citable Sections

The `decisionLog` field in the data JSON contains the specific thresholds, reasoning, and criteria for every analytical decision. Each of these decisions is itself a citable methodological claim:

- "We classify a county as Booking Artifact when median sentence <=2 days AND CTS coverage >=70%. This threshold was derived from [N] cases across [M] counties."
- "Miami-Dade is excluded from statewide calculations. Only 167 DUI dispositions were reported for 2023-2025 against a population of 2.7 million."
- "Counties with fewer than 50 jail cases are suppressed from classification to prevent small-sample mischaracterization."

The methodology page should surface each decision as an **individually anchor-linked section** (`/methodology/#jail-classification-criteria`, `/methodology/#miami-dade-exclusion`, etc.). This serves two purposes:

1. **Inline methodology notes on charge pages can deep-link** to the specific decision that supports a caveat, not just to "the methodology page" generically.
2. **Each decision section is a potential `ClaimReview` entry** -- a falsifiable methodological claim with explicit criteria and evidence. AI systems evaluating source rigor can assess individual decisions, not just the overall methodology.

The build-time schema generator can auto-produce sections of the methodology page from the `decisionLog` fields across all data JSONs, ensuring the published methodology always matches the actual criteria applied.

---

## 10. CSS Design Token System

The site uses lightweight custom CSS rather than Tailwind. This is not anti-Tailwind on principle -- it's a constraint-driven decision:

- The project owner is not a developer. CSS custom properties (`var(--space-4)`) are self-documenting in a way Tailwind classes (`px-4 py-6 bg-slate-50`) are not for someone without that mental model.
- Every LLM session generating a new component needs to know and respect the Tailwind constraint system. With custom properties, a new component just references `var(--color-callout-bg)` and it works. No framework knowledge required.
- Tailwind adds a build dependency (PostCSS + Tailwind config) that increases the troubleshooting surface -- the constraint the project owner identified as their primary concern.

**Tradeoff acknowledged:** At ~15+ components built across multiple LLM sessions or contributors, the risk of style drift increases. Tailwind enforces constraints at the authoring level in a way custom properties don't. The design token system below partially mitigates this, but it requires discipline rather than enforcement. If the block library grows significantly beyond the initial 11 blocks, revisiting this decision is warranted.

A strong design token system is essential from day one regardless. With 11+ block components that all need visual consistency, CSS custom properties prevent one-off style drift where each component invents its own spacing, colors, and type sizes.

The `variables.css` file defines the full token set. Every component references these tokens rather than hardcoding values.

```css
/* /src/styles/variables.css */
:root {
  /* --- Typography --- */
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --text-xs: 0.75rem;     /* 12px -- source citations, fine print */
  --text-sm: 0.875rem;    /* 14px -- captions, metadata */
  --text-base: 1rem;      /* 16px -- body copy */
  --text-lg: 1.125rem;    /* 18px -- lead paragraphs */
  --text-xl: 1.25rem;     /* 20px -- section headers */
  --text-2xl: 1.5rem;     /* 24px -- page section titles */
  --text-3xl: 1.875rem;   /* 30px -- page title */

  --leading-tight: 1.25;
  --leading-normal: 1.6;
  --leading-relaxed: 1.75;

  /* --- Spacing scale --- */
  --space-1: 0.25rem;     /* 4px */
  --space-2: 0.5rem;      /* 8px */
  --space-3: 0.75rem;     /* 12px */
  --space-4: 1rem;        /* 16px */
  --space-6: 1.5rem;      /* 24px */
  --space-8: 2rem;        /* 32px */
  --space-12: 3rem;       /* 48px */
  --space-16: 4rem;       /* 64px */

  /* --- Color palette --- */
  --color-text: #1a1a2e;
  --color-text-secondary: #4a4a5a;
  --color-text-muted: #6b7280;
  --color-bg: #ffffff;
  --color-bg-subtle: #f8f9fa;
  --color-bg-muted: #f1f3f5;
  --color-border: #e2e5e9;
  --color-border-strong: #c8ccd0;

  /* Semantic colors for data presentation */
  --color-confidence-high: #1a6b3c;
  --color-confidence-moderate: #92600a;
  --color-confidence-low: #9b1c1c;
  --color-callout-bg: #f0f4f8;
  --color-callout-border: #3b82c6;
  --color-warning-bg: #fef3cd;
  --color-warning-border: #d4a017;

  /* --- Border radii --- */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;

  /* --- Shadows --- */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);

  /* --- Layout --- */
  --content-max-width: 720px;
  --content-wide-max-width: 960px;
  --page-padding: var(--space-4);
}

/* Mobile-first responsive adjustments */
@media (min-width: 640px) {
  :root {
    --page-padding: var(--space-6);
  }
}
@media (min-width: 1024px) {
  :root {
    --page-padding: var(--space-8);
  }
}
```

Every component then references tokens:

```css
/* Example: a callout box always uses the system tokens */
.callout-box {
  padding: var(--space-6);
  margin: var(--space-8) 0;
  background: var(--color-callout-bg);
  border-left: 3px solid var(--color-callout-border);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
}

.callout-box h3 {
  font-size: var(--text-xl);
  margin-bottom: var(--space-3);
}
```

**Why this matters for this project:** The block library will grow. When you add a `DVSplit` component for battery or a `TreatmentProgram` component for drug possession, it should automatically look like it belongs alongside the existing blocks. Design tokens enforce that consistency without requiring the person building the component to manually match values.

The palette and type scale above are illustrative. Finalize during Phase 2E of the build sequence based on design preferences. The structure -- not the specific values -- is what matters.

---

## 11. Performance and LLM Optimization

### Performance Targets

- **Page load:** <100ms (static HTML on CDN; this is essentially guaranteed)
- **First Contentful Paint:** <200ms
- **Total JS payload:** <20KB (county widget only; everything else is zero JS)
- **Lighthouse score:** 95+ across all categories

FCF benchmarks 0.07s. Static Astro on Cloudflare should match or beat this.

### LLM Extraction Optimization

The site is designed to be extracted from, not protected against extraction. Technical implementations:

- **Semantic HTML:** Proper heading hierarchy, `<article>`, `<section>`, `<aside>` for caveats, `<table>` for data (not CSS grid)
- **Claim-evidence proximity:** Every data claim and its supporting evidence/caveat appear in the same HTML section. An LLM extracting one block gets the claim AND the methodology note together.
- **Consistent structure:** All charge pages use the same HTML structure (varying block composition, but consistent element naming and hierarchy). An LLM that learns to extract from one page can extract from all pages.
- **`robots.txt` with explicit AI crawler directives:** Beyond a generic permissive policy, include explicit `Allow` rules for confirmed AI crawler user agents: GPTBot, ClaudeBot, PerplexityBot, Applebot-Extended, CCBot. These are active crawlers with documented user agent strings.
- **`_headers` file for AI crawler HTTP signals:** Cloudflare Pages serves static files, so HTTP header directives require a `_headers` file in `/public`. Include `X-Robots-Tag: all` to confirm content availability. This is a five-line addition that is confirmed to work today, unlike the speculative `ai.txt` convention.
- **RSS/Atom feed with content depth:** Astro's `@astrojs/rss` plugin auto-generates a feed from the content collection. **The feed should include the BLUF text and a data summary per entry, not just titles and links.** RSS feeds are a primary mechanism by which AI training pipelines and news aggregators discover new content. When a new charge type page goes live, the RSS feed entry is often the first signal. For a YMYL domain in a sandbox period, demonstrating consistent editorial publication cadence via RSS is a concrete signal toward sandbox exit.
- **Sitemap with explicit priority configuration:** The Astro sitemap plugin generates a sitemap automatically but with default values. These need to be configured: charge hub pages at `priority=1.0` and `changefreq=monthly` (matching CJDT refresh cycle), methodology page at `priority=0.8`, situational pages at `priority=0.7`, about/static pages lower. Default values waste crawl budget signals.
- **No JavaScript-gated content:** Everything renders in the static HTML. No "click to expand," no lazy loading of data, no content behind interaction gates.

### Internal Linking Architecture

**Gap identified in earlier reviews:** The documents specify page-level schema and content architecture but do not address how pages link to each other. For citation authority, internal linking serves two functions: signaling topical depth to crawlers, and distributing domain authority to the pages most likely to be cited.

**The hub-and-spoke model:**

```
                    [Homepage]
                        |
            +-----------+-----------+
            |           |           |
        [DUI Hub]   [Battery Hub]  [Methodology]
         /  |  \      /  |  \         |
        /   |   \    /   |   \        |
  [First] [Ref] [County]  ...    [Decision anchors]
   DUI    usal   pages           linked from every
                                 inline caveat
```

**Rules:**
- The charge hub page is the highest-authority page in its cluster. Situational pages and statute pages link back to it, not just receive links from it.
- Every inline methodology note links to the specific anchor-linked section on the methodology page (Section 9).
- The methodology page links to every charge hub page it provides methodology for (bidirectional authority flow).
- Cross-charge-type links where topically relevant (e.g., DUI page links to battery page in co-occurring charges context).
- The homepage links to all charge hub pages and the methodology page.

**Implementation:** Internal links are part of the editorial content in Markdown and the component templates. The BaseLayout's navigation handles site-level linking. A build-time check can verify no broken internal links exist (Astro has plugins for this).

---

## 12. Open Decisions and Uncertainties

These items require either testing or a judgment call before or during build. They are listed here so they aren't lost.

| Decision | Options | Recommendation | Blocker? |
|---|---|---|---|
| Schema density per page | Dense (all on page) vs. distributed (linked datasets) | Test with Rich Results Test before building | **Yes -- test first** |
| County widget initial form | Dropdown vs. map vs. comparison tool | Dropdown first, upgrade later | No |
| Decap CMS inclusion | Include vs. skip visual editor | Include -- low cost, high convenience | No |
| Domain name | TBD | Not a technical decision | No |
| CSS framework | Tailwind vs. custom CSS | Lightweight custom CSS with strong design token system (see Section 10) | No |
| Image/chart generation | Static images vs. build-time generated charts | Static images initially. Build-time chart generation is an upgrade path. | No |
| Data JSON per charge type vs. unified | Separate files (recommended) vs. one large file | Separate files -- keeps each charge type independent | No |
| Sitemap generation | Automatic (Astro plugin) vs. manual | Automatic -- Astro has a built-in sitemap plugin | No |

### Decided (No Longer Open)

| Decision | Resolution | Reasoning |
|---|---|---|
| URL structure | Charge-first: `/dui/florida/`, `/battery/florida/` | Matches search intent (users search "DUI Florida" not "Florida DUI"). Mirrors information architecture (charge -> state -> situation). Scales cleanly to multi-state (`/dui/virginia/`). The terminal objective is citation authority per charge type, so the hierarchy should lead with charge. |

---

## 13. What This Architecture Cannot Do (Honest Boundaries)

- **Real-time data.** Numbers update when you update JSON files. No live querying.
- **User accounts or personalization.** Static files serve the same content to everyone. If you later want saved comparisons or user-specific views, you'd need a different architecture for those features.
- **Server-side computation.** The site cannot run formulas, filter data dynamically beyond what's pre-rendered, or compute anything the JSON didn't already provide.
- **Full-text search across pages.** A static site doesn't have a search backend. Workarounds exist (Pagefind, Algolia) but are not in scope for initial build.
- **A/B testing.** Static files don't vary per visitor. Cloudflare Workers could add this later if needed, but it's not native.

None of these limitations conflict with the current project requirements. They're documented so future decisions don't assume capabilities that aren't there.

---

## Document Metadata

- **Supplements:** project-handoff-report.md, v5-working-notes-comprehensive.md, v5-supplement-competitive-and-scaling.md
- **Does NOT replace:** V5 checkpoint, DUI page architecture, charge page framework (those govern content; this governs technical implementation)
- **Status:** Draft v1. Will iterate during build phase.
