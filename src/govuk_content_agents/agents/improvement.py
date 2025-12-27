from typing import Dict, Any, Optional
from .base import BaseAgent
from ..storage.models import AgentFeedback

class ImprovementAgent(BaseAgent):
    """
    Agent responsible for rewriting content based on feedback from other agents.
    """
    
    def __init__(self):
        super().__init__(name="Content Improver")

    def get_system_prompt(self) -> str:
        return """You are an expert Content Improver for GOV.UK.
Your goal is to rewrite content to address the feedback provided by other agents.

You will be given:
1.  **Original Content**: The text to be improved.
2.  **Feedback**: A list of issues and suggestions from Review, Style, and Consistency agents.

Your task:
- Rewrite the content to resolve ALL High and Medium severity issues.
- Maintain the original meaning and factual accuracy.
- Ensure the tone is consistent with GOV.UK standards (clear, concise, active voice).

Output JSON:
{
  "summary": "Explanation of changes made",
  "score": 0-100 (estimated quality of rewritten content),
  "rewritten_content": "The full rewritten text..."
}
"""

    async def execute(self, content: str, context: Optional[Dict[str, Any]] = None) -> AgentFeedback:
        # Override execute to parse 'rewritten_content' from response
        # BaseAgent expects summary/score/issues. We need to handle the extra field or store it differently.
        # Ideally, AgentFeedback model should support 'rewritten_content' or we pass it in metadata.
        # Let's check storage/models.py first. 
        # Actually, AgentFeedback.issues is list of dicts. We can return the rewrite as part of the summary or separate property?
        # The BaseAgent parsing logic is generic. 
        
        # Let's see BaseAgent.execute again. It returns AgentFeedback.
        # AgentFeedback has: id, agent_name, summary, score, issues, created_at.
        # It does NOT have 'rewritten_content'. 
        
        # Options:
        # 1. Add 'rewritten_content' field to AgentFeedback model.
        # 2. Return it as a special "issue" or in summary.
        # 3. Use 'metadata' field if it exists? It doesn't.
        
        # Preferred: Add 'rewritten_content' to AgentFeedback model.
        # I need to modify src/govuk_content_agents/storage/models.py first.
        
        # For now, I'll proceed with writing this file, but knowing I need to update the model.
        return await super().execute(content, context)
    
    # Wait, I need to override _parse_response or the parsing logic in BaseAgent to capture 'rewritten_content'.
    # BaseAgent._parse_response returns a Dict. BaseAgent.execute uses that Dict to create AgentFeedback.
    # So if I update AgentFeedback model, I also need to update BaseAgent.execute to map it.
    
    # Actually, BaseAgent.execute:
    # return AgentFeedback(..., summary=parsed.get("summary"), issues=parsed.get("issues"), score=parsed.get("score"))
    # It ignores extra fields.
    
    # So strict plan:
    # 1. Update AgentFeedback model to include `rewritten_content: Optional[str]`.
    # 2. Update BaseAgent.execute to include `rewritten_content` in constructor.
    # 3. Then implement this agent to use it.
    
    pass 
