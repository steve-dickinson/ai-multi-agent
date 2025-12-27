# GOV.UK Content AI Agents

> Multi-agent AI system for reviewing GOV.UK content with human oversight.

## Project Status: Stage 1 (Foundation)
Functional base agent and Content Reviewer agent implemented.
**Default Provider**: OpenAI (`gpt-4.1-mini`).
**Supported Providers**: OpenAI, Google Gemini.

## Features (Implemented)
- 🏗️ **Core Infrastructure**: Pydantic configuration, structured logging.
- 🤖 **Multi-Provider Agents**:
    - **OpenAI**: Default provider (`gpt-4.1-mini`) for reliable, fast responses.
    - **Gemini**: Supported fallback (`gemini-2.0-flash`) with automatic rate-limit retries.
- 📝 **Content Reviewer Agent**: Analyzes structure, clarity, and user needs using GOV.UK standards.
- 🗄️ **Database Layer**: Async MongoDB and PgVector clients ready for use.


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
    uv run python scripts/demo_stage_1.py
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
