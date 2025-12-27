# Capabilities & Advanced Features

This system goes beyond simple spell-checking. It employs a multi-agent architecture to simulate the entire content publishing workflow, from drafting to stress-testing.

## 1. The Persona Lab
> *"Don't just write for users—simulate them."*

Before you put content in front of a real user, test it in the Persona Lab. This feature simulates how different user archetypes interact with your content.

### Available Personas
*   **The Anxious User**: High stress, low patience. Misses details when overwhelmed.
*   **The Non-Native Speaker**: struggles with idioms, complex clauses, and "official" tone.
*   **The Skimmer**: Only reads headings and bold text. Fails if the answer is buried.

**How it works**: The agent adopts the persona's system prompt and attempts to "use" the content. It reports back an **Ease of Use Score (0-100)** and specific "Pain Points" where it got stuck or confused.

## 2. Debate Mode (Adversarial Review)
> *"Iron sharpens iron."*

Content design often involves balancing competing interests: legal accuracy vs. user simplicity. Debate Mode automates this tension.

### The Simplifier
*   **The Simplifier**: Ruthlessly cuts jargon. Wants an 8th-grade reading level.
*   **The Legalist**: Obsessed with precision. Fears liability. Wants every condition explicitly stated.
*   **The Mediator**: Synthesises the two arguments into a final version that is "as simple as possible, but no simpler."

**Value**: This provides a balanced perspective that a single human editor might miss.

## 3. Silo Breaker (Consistency Check)
> *"One Organisation, One Voice."*

A common problem in large organisations is contradictory advice across departments.

**How it works**:
1.  We store thousands of policy documents in a **pgvector** database.
2.  When you draft content, the **Consistency Agent** converts your text into vector embeddings.
3.  It performs a semantic search across the entire organisational knowledge base.
4.  **CRITICAL ALERT**: If your draft contradicts an existing policy, it is flagged as a High Severity issue.

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

## 5. Visual Analytics
> *"See the invisible."*

Text analysis tools often just give a score. Our **Tone Heatmap** visualizes the problem.

*   **<span style="color:red">Red</span>**: Passive Voice ("It was decided...").
*   **<span style="color:blue">Blue</span>**: Complex Words ("Utilize", "Facilitate").
*   **<span style="color:orange">Yellow</span>**: Sentences over 25 words.

This allows editors to scan a document in seconds and identify problem areas without reading every word.
