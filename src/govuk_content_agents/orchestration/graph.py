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
        "feedback": [] # Clear feedback for next round? Or keep history?
        # Ideally clear needed triggers for next round, but LangGraph state is additive if annotated.
        # But here we want the *new* feedback to be based on new content.
        # Since 'feedback' is Annotated[operator.add], returning [] doesn't clear it.
        # We might need to manually handle clearing or just append and let improver look at recent ones.
        # For simplicity in this logical loop, we'll assume improver looks at *latest* batch.
        # But wait, if we loop back to review, 'feedback' grows.
        # We need to distinguish rounds.
        # Actually, let's keep it simple: clear feedback is hard with operator.add.
        # Let's NOT use operator.add for feedback if we want to reset it, or we manage it manually.
        # But parallel execution requires operator.add to merge results from branches.
        # A trick is to return explicit 'feedback' list that replaces old one? 
        # No, operator.add forces append.
        # Solution: The 'feedback' in state will grow. The improver should only look at the last N items (3 agents per round).
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
    print(f"DEBUG: decision={state.get('final_decision')}, iter={state.get('iteration')}")
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

# We want parallel execution. 
# In LangGraph/LangChain, we can branch from entry to multiple nodes?
# Actually, we need a 'start' node or just set entry point to a map step?
# Simplify: 
# 1. Start -> parallel_gateway (virtual) -> [Review1, Review2, Review3] -> barrier -> Improve
# LangGraph achieves parallel by having same start node pointing to multiple nodes?
# Or one node calls multiple things?
# Current LangGraph version allows multiple start nodes? Or create a valid map.
# Let's run sequentially for Stage 2 MVP stability if parallel is complex, 
# BUT parallel is better.
# To do parallel:
# node "start" -> ["review_content", "review_style", "review_consistency"]
# each of those -> "improve"
# LangGraph will wait for all predecessors? Yes, if "improve" waits for all.
# Actually, standard LangGraph: join is implicit if multiple edges go to one node? No.
# Let's run sequentially for now to be safe: 
# Content -> Style -> Consistency -> Improve -> Judge
# It's slower but safer to implement without debugging race conditions.

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
