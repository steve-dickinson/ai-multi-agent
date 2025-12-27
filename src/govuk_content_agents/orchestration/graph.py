from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from .state import AgentState
from ..agents import (
    ContentReviewerAgent, 
    StyleComplianceAgent, 
    ConsistencyAgent, 
    ImprovementAgent, 
    QualityJudgeAgent
)
from ..storage.models import AgentFeedback

# Initialize agents
content_agent = ContentReviewerAgent()
style_agent = StyleComplianceAgent()
consistency_agent = ConsistencyAgent()
improvement_agent = ImprovementAgent()
judge_agent = QualityJudgeAgent()

async def review_content(state: AgentState):
    """Run Content Reviewer."""
    feedback = await content_agent.execute(state["current_content"])
    return {"feedback": [feedback]}

async def review_style(state: AgentState):
    """Run Style Check."""
    feedback = await style_agent.execute(state["current_content"])
    return {"feedback": [feedback]}

async def review_consistency(state: AgentState):
    """Run Consistency Check."""
    feedback = await consistency_agent.execute(state["current_content"])
    return {"feedback": [feedback]}

async def improve_content(state: AgentState):
    """Generate improved content based on feedback."""
    feedback_summary = [
        {"agent": f.agent_name, "issues": f.issues} 
        for f in state["feedback"]
    ]
    
    result = await improvement_agent.execute(
        state["current_content"], 
        context={"feedback": feedback_summary}
    )
    
    new_content = result.rewritten_content if result.rewritten_content else state["current_content"]
    
    return {
        "current_content": new_content,
        "iteration": state["iteration"] + 1,
        "feedback": [] 
    }

async def judge_content(state: AgentState):
    """Score the content."""
    result = await judge_agent.execute(state["current_content"])
    decision = "pass" if (result.score or 0) >= 80 else "fail"
    return {
        "final_score": result.score, 
        "final_decision": decision
    }

def router(state: AgentState):
    """Decide whether to loop or end."""
    if state.get("final_decision") == "pass" or state["iteration"] >= state["max_iterations"]:
        return "stop"
    else:
        return "continue_loop"

# Build Graph
builder = StateGraph(AgentState)

# Nodes
builder.add_node("review_content", review_content)
builder.add_node("review_style", review_style)
builder.add_node("review_consistency", review_consistency)
builder.add_node("improve", improve_content)
builder.add_node("judge", judge_content)

# Flow
# Start -> Parallel Reviews
builder.set_entry_point("review_content")
builder.add_edge("review_content", "improve")

# Sequential execution flow
builder.set_entry_point("review_content")
builder.add_edge("review_content", "review_style")
builder.add_edge("review_style", "review_consistency")
builder.add_edge("review_consistency", "improve")
builder.add_edge("improve", "judge")

# Conditional Edge
builder.add_conditional_edges(
    "judge",
    router,
    {
        "continue_loop": "review_content",
        "stop": END
    }
)

app = builder.compile()
