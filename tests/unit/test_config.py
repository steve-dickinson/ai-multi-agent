import pytest
from govuk_content_agents.config import Settings

def test_settings_load():
    """Test that settings load correctly from env vars."""
    settings = Settings()
    assert settings.GEMINI_API_KEY == "sk-gemini-test-key"
    assert settings.APP_NAME == "GOV.UK Content Agents"
