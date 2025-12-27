# AI Multi-Agent Content System

**Automated content operations for digital services.**

This platform acts as an intelligent pair-programmer for content designers. It uses a team of specialised AI agents to ensure every piece of content is clear, consistent with policy, and accessible to all users.

## Why use this system?

*   **Empower content designers**: Automate routine checks (style guide, passive voice) to aid humans in focusing on strategy.
*   **Prevent policy conflicts**: The [Silo Breaker](capabilities.md#3-silo-breaker-consistency-check) agent catches contradictions across departments.
*   **Simulate user research**: The [Persona Lab](capabilities.md#1-the-persona-lab) tests your content against anxious or non-native users instantly.

## The Solution: A Team of Specialists

This system solves the "Messy Middle" of content operations by assigning distinct specialist roles to AI agents:

1.  **The Ingest Agent** 📥
    *   **Problem**: Source material is everywhere (PDFs, URLs, APIs).
    *   **Solution**: Unifies input from Text, URLs, and the GOV.UK Content API into a standardized format.

2.  **The Content Architect** 📐
    *   **Problem**: Blank page syndrome leads to inconsistent structures.
    *   **Solution**: Generates drafts using official templates (Start Pages, Guides) to structure user needs *before* writing begins.

3.  **The Core Review Engine** 🛡️
    *   **Problem**: Routine compliance checks consume valuable design time.
    *   **Solution**: Rigorously checks Style Guide compliance, structure, and readability (Inverted Pyramid) automatically.

4.  **The Debate Club** 🥊
    *   **Problem**: Balancing legal accuracy with simplicity is hard.
    *   **Solution**: Pits a "Simplifier" agent against a "Legalist" agent. A "Mediator" synthesises the best of both.

5.  **The Silo Breaker** 🏗️
    *   **Problem**: Content often contradicts policies from other departments.
    *   **Solution**: Uses Vector Search to find conflicts across the entire organisational knowledge base (e.g., Forestry vs Peatland).

6.  **The Persona Lab** 🥼
    *   **Problem**: We forget how confusing content is for stressed users.
    *   **Solution**: Simulates "Anxious" or "Non-Native" users to test content comprehension before publication.

[Explore Detailed Capabilities &rarr;](capabilities.md)

## User Guide

### Using the Interface
The system provides a **Streamlit** dashboard for easy interaction.

1.  **Launch**: `uv run streamlit run src/govuk_content_agents/ui/app.py`
2.  **Input Methods**: (Available on ALL pages)
    *   **Text**: Paste raw draft content.
    *   **URL**: Enter a web page URL.
    *   **GOV.UK API**: Enter a path (e.g., `/vat-rates`).
3.  **Workflows**:
    *   **Analyze**: Use the dashboard to get a full report.
    *   **Debate**: Pit agents against each other to find the balance between simplicity and accuracy.
    *   **Simulate**: See your content through the eyes of an "Anxious User".

---
*Disclaimer: This is a personal experimentation project to explore the capabilities of AI agents in content workflows. It is not an official tool and is not currently in use by any department.*

