import pytest
from unittest.mock import MagicMock, patch
from govuk_content_agents.agents.quality_judge import QualityJudgeAgent

@pytest.mark.asyncio
async def test_quality_judge_execution():
    """Test Quality Judge Agent execution."""
    
    mock_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = """
    {
        "summary": "Excellent content.",
        "score": 95,
        "issues": []
    }
    """
    mock_openai.chat.completions.create.return_value = mock_response

    with patch("govuk_content_agents.agents.base.OpenAI", return_value=mock_openai):
        agent = QualityJudgeAgent()
        result = await agent.execute("Perfect content")
        
        assert result.agent_name == "Quality Judge"
        assert result.score == 95
