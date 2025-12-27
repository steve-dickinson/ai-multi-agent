from typing import Any, Dict, List, Union
from .base import BaseAgent
from ..data.personas import PERSONAS

class PersonaAgent(BaseAgent):
    """
    Agent that simulates a specific user persona reading content.
    """
    
    def __init__(self):
        super().__init__(name="Persona Simulator")
        self.current_persona_key = "anxious" # Default

    def set_persona(self, persona_key: str):
        if persona_key not in PERSONAS:
            raise ValueError(f"Unknown persona: {persona_key}")
        self.current_persona_key = persona_key

    def get_system_prompt(self) -> str:
        persona = PERSONAS[self.current_persona_key]
        return f"""
{persona['system_prompt']}

RESPONSE FORMAT:
You must return a JSON object with:
- "summary": A first-person account of your experience reading the content.
- "score": An 'Ease of Use' score from 0-100 based on YOUR persona's ability to cope.
- "issues": A list of dictionaries, where each issue has:
    - "description": "The specific text or trigger that caused the problem"
    - "severity": "High" or "Medium" or "Low"
- "rewritten_content": null (you are a reader, not a writer).
"""

    async def execute(self, content: str, context: dict = None):
        # We override execute/parse or just rely on BaseAgent but ensure types are correct.
        # Since BaseAgent calls _parse_response which returns raw dict, 
        # and then instantiates AgentFeedback, we might receive issues as List[str] from LLM 
        # even if we ask for dicts (LLMs can be flaky).
        
        # To be safe, let's catch the output of base call, but wait...
        # BaseAgent.execute calls _execute_openai which instantiates AgentFeedback IMMEDIATELY.
        # If instantiation fails, it raises the error seen.
        
        # So we MUST subclass _execute_openai or ensure the LLM output is robust.
        # OR we can patch `_parse_response` in this instance.
        
        # Easiest fix: Override_parse_response to normalize issues.
        return await super().execute(content, context)

    def _parse_response(self, text: str) -> Dict[str, Any]:
        """Parse JSON response and normalize issues."""
        data = super()._parse_response(text)
        
        # Normalize issues if they are strings
        issues = data.get("issues", [])
        normalized_issues = []
        for issue in issues:
            if isinstance(issue, str):
                normalized_issues.append({
                    "description": issue,
                    "severity": "Medium", # Default
                    "suggestion": "Review tone" 
                })
            elif isinstance(issue, dict):
                # Normalize keys to lowercase to avoid UI issues
                clean_issue = {}
                # Find content
                clean_issue["description"] = issue.get("description") or issue.get("Description") or issue.get("issue") or issue.get("text") or "Unknown issue"
                # Find severity
                clean_issue["severity"] = issue.get("severity") or issue.get("Severity") or "Medium"
                
                normalized_issues.append(clean_issue)
        
        data["issues"] = normalized_issues
        return data
