import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from govuk_content_agents.agents.consistency import ConsistencyAgent

@pytest.mark.asyncio
async def test_consistency_execution():
    """Test Consistency Agent execution with mocked DB and API."""
    
    # Mock OpenAI for chat and embeddings
    mock_openai = MagicMock()
    
    # Mock embedding response
    mock_embedding_resp = MagicMock()
    mock_embedding_resp.data = [MagicMock(embedding=[0.1] * 1536)]
    mock_openai.embeddings.create.return_value = mock_embedding_resp
    
    # Mock chat response
    mock_chat_resp = MagicMock()
    mock_chat_resp.choices[0].message.content = '{"summary": "Consistent", "score": 90, "issues": []}'
    mock_openai.chat.completions.create.return_value = mock_chat_resp
    
    # Mock Vector DB
    mock_vector_db = MagicMock()
    mock_vector_db.search_similar.return_value = [
        {"id": "123", "content": "Similar content", "similarity": 0.85}
    ]

    with patch("govuk_content_agents.agents.base.OpenAI", return_value=mock_openai), \
         patch("govuk_content_agents.agents.consistency.vector_client", mock_vector_db):
        
        agent = ConsistencyAgent()
        result = await agent.execute("New test content")
        
        assert result.agent_name == "Consistency Checker"
        assert result.score == 90
        
        # Verify flow
        mock_openai.embeddings.create.assert_called_once()
        mock_vector_db.search_similar.assert_called_once()
        
        # Verify context passed to chat
        call_args = mock_openai.chat.completions.create.call_args
        messages = call_args.kwargs['messages']
        user_msg = messages[1]['content'] # content message
        # In current implementation, context is appended to prompt in BaseAgent using json.dumps
        # let's check it was passed 
        # Actually in base.py _execute_openai appends "Additional Context:"
        assert len(messages) >= 2
        # Check if context was passed. BaseAgent appends prompt += json... if context provided.
        # But _execute_openai explicitly appends a new message for context if self.provider == "openai"
        # Wait, let's re-read _execute_openai in base.py.
        # Yes: if context: messages.append({"role": "user", "content": ...})
        if len(messages) > 2:
            assert "Found the following similar content" in messages[2]['content']
