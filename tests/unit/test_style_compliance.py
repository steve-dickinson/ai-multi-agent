import pytest
from unittest.mock import MagicMock, patch
from govuk_content_agents.agents.style_compliance import StyleComplianceAgent

@pytest.mark.asyncio
async def test_style_compliance_execution():
    """Test Style Compliance Agent execution with mocked API."""
    
    mock_openai = MagicMock()
    mock_response = MagicMock()
    # Mocking a response detecting passive voice
    mock_response.choices[0].message.content = """
    {
        "summary": "Found passive voice usage.",
        "score": 75,
        "issues": [
            {
                "severity": "medium",
                "description": "Passive voice detected: 'Mistakes were made'.",
                "suggestion": "Use active voice: 'I made mistakes'."
            }
        ]
    }
    """
    mock_openai.chat.completions.create.return_value = mock_response

    with patch("govuk_content_agents.agents.base.OpenAI", return_value=mock_openai):
        agent = StyleComplianceAgent()
        result = await agent.execute("Mistakes were made.")
        
        assert result.agent_name == "Style & Compliance"
        assert result.score == 75
        assert len(result.issues) == 1
        assert "Passive voice" in result.issues[0]["description"]
