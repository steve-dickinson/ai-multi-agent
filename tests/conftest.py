import pytest
import os
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture(scope="session", autouse=True)
def mock_env_vars():
    """Set mock environment variables for testing."""
    os.environ["GEMINI_API_KEY"] = "sk-gemini-test-key"
    os.environ["OPENAI_API_KEY"] = "sk-openai-test-key"
    os.environ["MONGO_URI"] = "mongodb://localhost:27017"
    os.environ["POSTGRES_URI"] = "postgresql://user:pass@localhost:5432/db"
    
@pytest.fixture
def mock_gemini():
    """Mock Gemini client."""
    mock_client = MagicMock()
    mock_models = MagicMock()
    mock_client.models = mock_models
    
    # Setup default response
    mock_response = MagicMock()
    mock_response.text = '{"summary": "Test", "score": 80, "issues": []}'
    mock_models.generate_content.return_value = mock_response
    
    return mock_client
