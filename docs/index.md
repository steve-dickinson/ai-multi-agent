# AI Multi-Agent Content System

> *Disclaimer: This is an experimental research project. It is **not** affiliated with GOV.UK.*

**Automated content operations for digital services.**

This platform acts as an intelligent pair-programmer for content designers. It uses a team of specialised AI agents to ensure every piece of content is clear, consistent with policy, and accessible to all users.

## Why use this system?

*   **Reduce specialised labour**: Automate the routine checks (style guide, passive voice) so humans can focus on strategy.
*   **Prevent policy conflicts**: The [Silo Breaker](capabilities.md#3-silo-breaker-consistency-check) agent catches contradictions across departments.
*   **Simulate user research**: The [Persona Lab](capabilities.md#1-the-persona-lab) tests your content against anxious or non-native users instantly.

## The Agent Team

The system is powered by a graph of specialised agents:

1.  **Content Reviewer**: Checks structure and user needs.
2.  **Style Compliance**: Enforces style rules.
3.  **Consistency**: Checks for duplication against the vector database.
4.  **Improver**: Rewrites the content to fix issues.
5.  **Judge**: Scores the final output.

[Explore all Capabilities &rarr;](capabilities.md)

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

