import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from govuk_content_agents.orchestration.graph import app
from govuk_content_agents.storage.models import AgentFeedback

@pytest.mark.asyncio
async def test_graph_execution_flow():
    """Test full graph execution with mocked agents."""
    
    # Mock return values for each agent
    mock_feedback = AgentFeedback(agent_name="Test", summary="Safe", issues=[], score=90)
    
    # We need to patch the agents instantiated in graph.py
    # Since they are imported and instantiated at module level, we must patch where they are used or imported
    
    with patch("govuk_content_agents.orchestration.graph.content_agent.execute", new_callable=AsyncMock) as m_content, \
         patch("govuk_content_agents.orchestration.graph.style_agent.execute", new_callable=AsyncMock) as m_style, \
         patch("govuk_content_agents.orchestration.graph.consistency_agent.execute", new_callable=AsyncMock) as m_const, \
         patch("govuk_content_agents.orchestration.graph.improvement_agent.execute", new_callable=AsyncMock) as m_improv, \
         patch("govuk_content_agents.orchestration.graph.judge_agent.execute", new_callable=AsyncMock) as m_judge:
        
        # Setup mocks
        m_content.return_value = AgentFeedback(agent_name="Content", summary="Ok", score=80)
        m_style.return_value = AgentFeedback(agent_name="Style", summary="Ok", score=80)
        m_const.return_value = AgentFeedback(agent_name="Consistency", summary="Ok", score=80)
        
        # Improvement returns rewritten content
        m_improv.return_value = AgentFeedback(agent_name="Improver", summary="Fixed", score=90, rewritten_content="Better content")
        
        # Judge passes it
        m_judge.return_value = AgentFeedback(agent_name="Judge", summary="Good", score=90)
        
        # Run Graph
        initial_state = {
            "input_content": "Draft content",
            "current_content": "Draft content",
            "feedback": [],
            "iteration": 0,
            "max_iterations": 2,
            "metadata": {}
        }
        
        final_state = await app.ainvoke(initial_state)
        
        # Verify result
        assert final_state["final_decision"] == "pass"
        assert final_state["current_content"] == "Better content"
        assert final_state["iteration"] == 1
        
        # Verify all agents called
        m_content.assert_called()
        m_style.assert_called()
        m_const.assert_called()
        m_improv.assert_called()
        m_judge.assert_called()
