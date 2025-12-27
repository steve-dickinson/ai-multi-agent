FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml .

# Install dependencies (system-wide)
# Using --system flag for uv pip install or just install directly
RUN uv pip install --system . --no-cache

# Copy application code
COPY src src
COPY scripts scripts

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "src/govuk_content_agents/ui/app.py"]
