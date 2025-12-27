from typing import Any, Dict, Optional
from .base import BaseAgent
import json

class SimplifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="The Simplifier")

    def get_system_prompt(self) -> str:
        return """You are The Simplifier.
Your ONLY goal is to make the content easier to read.
You hate jargon, long sentences, and complex clauses.
You are willing to sacrifice some nuance for clarity.
Review the content and ruthlessly cut it down.

Output JSON:
{
  "summary": "Why this needs simplifying",
  "rewritten_content": "The simplified version",
  "issues": []
}
"""

class LegalistAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="The Legalist")

    def get_system_prompt(self) -> str:
        return """You are The Legalist.
Your ONLY goal is accuracy and precision.
You are terrified of the government being sued for misleading advice.
You PREFER long sentences if they ensure there is no ambiguity.
You hate "dumbing down" if it removes necessary conditions.
Review the content and Rewrite it to be 100% legally watertight.

Output JSON:
{
  "summary": "Why the simplified view is dangerous/inaccurate",
  "rewritten_content": "The precise version",
  "issues": []
}
"""

class MediatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="The Mediator")

    def get_system_prompt(self) -> str:
        return """You are The Mediator.
You have listed to two arguments:
1. The Simplifier (who wants it easy).
2. The Legalist (who wants it precise).

Your goal is to synthesize a FINAL VERSION that achieves the best of both worlds.
- It must be as simple as possible...
- ...but NOT simplier than the law allows.

Output JSON:
{
  "summary": "How you balanced the two views",
  "rewritten_content": "The final synthesized version",
  "issues": []
}
"""

    async def mediate(self, original: str, simplified: str, legal: str) -> Dict[str, Any]:
        """Special execution method that takes all inputs."""
        prompt = f"""
ORIGINAL CONTENT:
{original}

---
ARGUMENT A (THE SIMPLIFIER):
{simplified}

---
ARGUMENT B (THE LEGALIST):
{legal}

---
DECISION:
Synthesize the final version.
"""
        # Execute using standard calling convention but with the constructed prompt
        feedback = await self.execute(prompt)
        return {
            "summary": feedback.summary,
            "final_content": feedback.rewritten_content
        }
