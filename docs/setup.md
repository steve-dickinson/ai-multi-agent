# Setup Guide

## Prerequisites
- **Python 3.13+**
- **uv**: High-performance Python package installer. [Install guide](https://github.com/astral-sh/uv).
- **Docker**: For running MongoDB and PostgreSQL databases.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/steve-dickinson/ai-multi-agent.git
    cd ai-multi-agent
    ```

2.  **Install dependencies**:
    ```bash
    uv sync
    ```

## Configuration

The application is configured using environment variables defined in `.env`.

1.  **Create .env file**:
    ```bash
    cp .env.example .env
    ```

2.  **API Keys**:
    *   **Required**: `OPENAI_API_KEY` for the default `gpt-4.1-mini` model.
    *   **Optional**: `GEMINI_API_KEY` if you wish to use Gemini models.

3.  **Databases**:
    The default configuration connects to local Docker instances:
    *   MongoDB: `mongodb://admin:password@localhost:27018`
    *   PostgreSQL: `postgresql://admin:password@localhost:5432/ai_agent_db`

## Running Locally

1.  **Start Infrastructure**:
    ```bash
    docker-compose up -d
    ```

2.  **Run the App**:
    ```bash
    uv run streamlit run src/govuk_content_agents/ui/app.py
    ```
