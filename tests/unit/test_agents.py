import pytest
from unittest.mock import patch, MagicMock
from govuk_content_agents.agents.content_reviewer import ContentReviewerAgent

@pytest.mark.asyncio
async def test_content_reviewer_execution_openai():
    """Test Content Reviewer execution with mocked OpenAI API."""
    
    mock_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '{"summary": "Test", "score": 80, "issues": []}'
    mock_openai.chat.completions.create.return_value = mock_response

    with patch("govuk_content_agents.agents.base.OpenAI", return_value=mock_openai):
        agent = ContentReviewerAgent()  # defaults to gpt-4o-mini
        result = await agent.execute("Test content")
        
        assert result.agent_name == "Content Reviewer"
        assert result.score == 80
        assert result.summary == "Test"
        assert agent.provider == "openai"
        
        # Verify API called with prompt
        mock_openai.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_agent_json_parsing_error_openai():
    """Test handling of invalid JSON response from OpenAI."""
    
    mock_openai = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = 'Invalid JSON'
    mock_openai.chat.completions.create.return_value = mock_response
    
    with patch("govuk_content_agents.agents.base.OpenAI", return_value=mock_openai):
        agent = ContentReviewerAgent()
        result = await agent.execute("Test content")
        
        # Should fallback to text summary
        assert result.summary == "Invalid JSON"
        assert result.issues == []
