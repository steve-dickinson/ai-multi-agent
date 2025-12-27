# AI Multi-Agent Content System (Experimental)

> **Experimental project exploring AI for content operations.**
> *Disclaimer: This is a personal research project. It is **not** affiliated with, endorsed by, or used by GOV.UK or the Government Digital Service. It is not a production service.*

## Overview
This platform explores how AI agents could act as an intelligent pair-programmer for content designers. It uses a team of specialized agents to review content against style guides (inspired by GDS consistency standards) to ensure clarity and accessibility.

## Features (Implemented)
- **Core Infrastructure**: Pydantic configuration, structured logging.
- **Multi-Provider Agents**: OpenAI (Default) & Gemini (Fallback).
- **Smart Orchestration**: LangGraph-based feedback loop.
- **Content Architect**: Template-based generation for Start Pages, Guides, and Answers.
- **Persona Lab**: Simulate user experiences (e.g., "Anxious User", "Non-Native Speaker").
- **Debate Mode**: "The Simplifier" vs "The Legalist" propose edits, and a Mediator synthesises the best version.
- **Silo Breaker**: Cross-policy checking (demonstrates matching against diverse datasets).
- **Knowledge Base Manager**: Dynamic UI to import policies from Text, URLs, or APIs.
- **Visual Analytics**: Heatmaps for passive voice/sentence length and semantic diffs.
- **Team of Agents**:
    - **Content Reviewer**: Structure & Clarity.
    - **Style Compliance**: Enforces style rules.
    - **Consistency**: Vector-based semantic duplication check.
    - **Improvement**: Auto-rewriting.
    - **Judge**: Final quality scoring.
- **Human-in-the-Loop UI**: Streamlit dashboard for interactive reviews.
- **Dynamic Inputs**:
    - Supported on **ALL** pages (Review, Lab, Debate, Analytics).
    - Raw Text
    - URL Web Scraping
    - GOV.UK Content API Integration
- **Database Layer**: Async MongoDB and PgVector.


### Running the UI
The Streamlit interface allows you to interact with the agent team interactively.
You can enter text directly, **fetch content from a URL**, or use the **GOV.UK Content API**.

```bash
uv run streamlit run src/govuk_content_agents/ui/app.py
```

Or via Docker:
```bash
docker compose up --build
```
Access the app at http://localhost:8501.

## Quick Start


### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (for package management)
- Docker & Docker Compose

### Fast Setup
1.  **Clone and Install**:
    ```bash
    git clone <repo-url>
    cd ai-multi-agent
    uv sync
    ```

2.  **Configure Environment**:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and add your **OPENAI_API_KEY**.
    *(Optional: Add `GEMINI_API_KEY` if you want to use Google Gemini)*

3.  **Start Databases**:
    ```bash
    docker-compose up -d
    ```

4.  **Launch the App**:
    ```bash
    uv run streamlit run src/govuk_content_agents/ui/app.py
    ```

## Development

### Running Tests
```bash
uv run pytest
```

### Documentation
Full documentation is available in the `docs/` directory.
To serve locally:
```bash
uv run mkdocs serve
```
