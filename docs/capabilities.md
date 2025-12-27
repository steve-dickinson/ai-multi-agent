# Capabilities & Advanced Features

This system goes beyond simple spell-checking. It employs a multi-agent architecture to simulate the entire content publishing workflow, from drafting to stress-testing.

## 0. The Ingest Agent (Unified Input)
> *"Start anywhere."*

The messy reality of government content is that source material comes in many formats. The Ingest Agent standardizes this.

*   **URL Fetching**: Scrape live content (e.g., EU Law text) directly.
*   **GOV.UK API**: Fetch structured content by path (e.g., `/vat-rates`).
*   **Text**: Paste raw drafts from emails or Word docs.

**Result**: A unified clean text format for the rest of the agents to work on.

## 1. The Persona Lab
> *"Don't just write for users—simulate them."*

Before you put content in front of a real user, test it in the Persona Lab. This feature simulates how different user archetypes interact with your content.

### Available Personas
*   **The Anxious User ("Skipper Tom")**: High stress, low patience. Simulates a user with a deadline (e.g., checking quotas at sea).
*   **The Non-Native Speaker**: Struggles with idioms, complex clauses, and "official" tone.
*   **The Skimmer**: Only reads headings and bold text. Fails if the answer is buried.

**How it works**: The agent adopts the persona's system prompt and attempts to "use" the content. It reports specific "Pain Points" where it got stuck (e.g., "I can't find Area VII in this PDF").

## 2. Debate Mode (Adversarial Review)
> *"Iron sharpens iron."*

Content design often involves balancing competing interests: legal accuracy vs. user simplicity. Debate Mode automates this tension.

### Example: Nutrient Neutrality
*   **The Simplifier**: "Just say 'stopping pollution entering the river'. Cut the jargon."
*   **The Legalist**: "We must specify 'total nitrogen load mitigation strategies' or we risk legal challenge."
*   **The Mediator**: Synthesises the two: "Use the legal term once for precision, then explain it simply."

**Value**: This provides a balanced perspective that a single human editor might miss.

## 3. Silo Breaker (Consistency Check)
> *"One Organisation, One Voice."*

A common problem in large organisations is contradictory advice across departments.

**How it works**:
1.  We store thousands of policy documents (e.g., Forestry Commission, Natural England) in a **pgvector** database.
2.  When you draft content (e.g., "Planting Trees"), the **Consistency Agent** converts your text into vector embeddings.
3.  It performs a semantic search across the entire organisational knowledge base.
4.  **CRITICAL ALERT**: If your draft contradicts an existing policy (e.g., "Planting prohibited on deep peat"), it is flagged as a High Severity issue.

### Knowledge Base Manager
To keep this data fresh, the **Knowledge Base Manager** allows you to:
- **Import Content**: Scrape live URLs, fetch from APIs, or paste text.
- **Tag Data**: Assign departments (e.g., HMRC, DWP) to track cross-org conflicts.
- **Real-time Indexing**: New policies are immediately vectorised and available for consistency checks.

## 4. The Content Architect
> *"Standardisation by default."*

Don't start from a blank page. The Content Architect uses proven patterns (Start Pages, Guides) to generate high-quality first drafts based on a simple user brief.

*   **Start Pages**: Ensures the "Before you start" section is present.
*   **Detailed Guides**: Enforces correct heading hierarchy.
*   **Answers**: optimized for featured snippets (bold direct answer first).

## 4a. The Core Review Engine (Quality Control)
> *"Hygiene before nuance."*

Before meaningful debate can happen, we must ensure basic compliance. This engine runs automated checks:

*   **Structure**: Checks for the "Inverted Pyramid" (main point first).
*   **User Needs**: Verifies the content addresses a clear user goal.
*   **Style**: Checks against the GDS Style Guide (e.g., "dispatch" vs "send").

## 5. Visual Analytics (Actionable Feedback)
> *"See the invisible."*

Text analysis tools often just give a score. Our system visualizes the problem by listing specific text segments that need fixing.

*   **Passive Voice**: Flags use of "It was decided..." vs "We decided".
*   **Complex Words**: Flags bureaucratic language like "Utilize" or "Facilitate".
*   **Sentence Length**: Highlights sentences over 25 words that are hard to read.

*Note: Future versions will include visual heatmaps directly on the canvas.*
This allows editors to scan a document in seconds and identify problem areas without reading every word.

---
*Disclaimer: This is a personal experimentation project to explore the capabilities of AI agents in content workflows. It is not an official tool and is not currently in use by any department.*
