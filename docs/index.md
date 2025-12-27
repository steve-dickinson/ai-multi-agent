# GOV.UK Content AI Agents

Welcome to the documentation for the Multi-Agent Content Review System.

## Overview

This system uses a team of specialized AI agents to review and improve content against GOV.UK standards.

### Agents (Stage 2)

- **Content Reviewer**: Checks structure, clarity, and user need focus.
- **Style Compliance**: Enforces GOV.UK specific style guide rules (passive voice, sentence length).
- **Consistency**: Uses Vector Search to ensure new content doesn't contradict or duplicate existing content.
- **Improvement**: Automatically rewrites content based on feedback from other agents.
- **Quality Judge**: The final decision maker that scores content (0-100) and approves/rejects it.

## User Guide

### Using the Interface
The system provides a **Streamlit** dashboard for easy interaction.

1.  **Launch**: `uv run streamlit run src/govuk_content_agents/ui/app.py`
2.  **Input Methods**:
    *   **Text**: Paste raw draft content.
    *   **URL**: Enter a web page URL (e.g., existing content to review). The system will scrape and clean the text.
    *   **GOV.UK API**: Enter a path (e.g., `/vat-rates`). The system will query the GOV.UK Content API, automatically handling standard pages and multi-part guides.
3.  **Generate**: Use the "Content Architect" (Create) page to build new drafts from official templates.
4.  **Review**: Watch the agents analyze and rewrite the content.
    *   *Note*: The **Silo Breaker** automatically checks for contradictions against HMRC/DWP policies during this step.
5.  **Simulate**: Use the "Persona Lab" page to see how an "Anxious User" or "Non-Native Speaker" interprets the content.
6.  **Debate**: Use the "Debate Mode" page to watch two agents fight over simplicity vs. legal accuracy.
7.  **Analyze**: Use the "Analytics" page to see Heatmaps (for tone) and Diffs (for changes).
8.  **Decision**: Use the "Review Queue" page to Approve or Reject the final output.

