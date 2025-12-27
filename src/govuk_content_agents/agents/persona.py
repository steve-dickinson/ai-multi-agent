from typing import Any, override
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

    @override
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

    @override
    def _parse_response(self, text: str) -> dict[str, Any]:
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
