# GOV.UK Content AI Agents

> Multi-agent AI system for reviewing GOV.UK content with human oversight.

## Project Status: Stage 3 (Production Ready)
Full multi-agent system implemented with Streamlit UI and Docker containers.
**Default Provider**: OpenAI (`gpt-4.1-mini`).
**Supported Providers**: OpenAI, Google Gemini.

## Features (Implemented)
- 🏗️ **Core Infrastructure**: Pydantic configuration, structured logging.
- 🤖 **Multi-Provider Agents**: OpenAI (Default) & Gemini (Fallback).
- 🧠 **Smart Orchestration**: LangGraph-based feedback loop.
- 🏗️ **Content Architect**: Template-based generation for Start Pages, Guides, and Answers.
- 🧪 **Persona Lab**: Simulate user experiences (e.g., "Anxious User", "Non-Native Speaker").
- ⚖️ **Debate Mode**: "The Simplifier" vs "The Legalist" propose edits, and data Mediator synthesizes the best version.
- 🏛️ **Silo Breaker**: Cross-department policy checking (matches against HMRC, DWP etc.).
- 👥 **Team of Agents**:
    - **Content Reviewer**: Structure & Clarity.
    - **Style Compliance**: GOV.UK Styleguide rules.
    - **Consistency**: Vector-based semantic duplication check.
    - **Improvement**: Auto-rewriting.
    - **Judge**: Final quality scoring.
- 🖥️ **Human-in-the-Loop UI**: Streamlit dashboard for interactive reviews.
- 🔌 **Dynamic Inputs**:
    - Raw Text
    - URL Web Scraping
    - GOV.UK Content API Integration
- 🗄️ **Database Layer**: Async MongoDB and PgVector.


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
- Python 3.11+
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

4.  **Run the Demo**:
    ```bash
    uv run python scripts/demo_stage_2.py
    ```
    Or run the UI:
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
