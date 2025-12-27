from typing import List, Dict, Any, Optional, TypedDict, Annotated
import operator
from ..storage.models import AgentFeedback

class AgentState(TypedDict):
    """
    Shared state for the multi-agent workflow.
    """
    input_content: str
    metadata: Dict[str, Any]
    
    # Feedback from parallel review node
    # Annotated[list, operator.add] means new feedback is appended to the list
    feedback: Annotated[List[AgentFeedback], operator.add]
    
    # Current working version of content (starts as input, then rewritten)
    current_content: str
    
    # Final outputs
    final_score: Optional[int]
    final_decision: Optional[str] # "pass" or "fail"
    
    # Loop control
    iteration: int
    max_iterations: int
