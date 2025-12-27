import pytest
from unittest.mock import MagicMock, patch
from govuk_content_agents.agents.improvement import ImprovementAgent

@pytest.mark.asyncio
async def test_improvement_execution():
    """Test Improvement Agent execution."""
    
    mock_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = """
    {
        "summary": "Improved clarity.",
        "score": 95,
        "rewritten_content": "This is the improved text."
    }
    """
    mock_openai.chat.completions.create.return_value = mock_response

    with patch("govuk_content_agents.agents.base.OpenAI", return_value=mock_openai):
        agent = ImprovementAgent()
        result = await agent.execute("Original text", context={"feedback": ["issue 1", "issue 2"]})
        
        assert result.agent_name == "Content Improver"
        assert result.score == 95
        assert result.rewritten_content == "This is the improved text."
