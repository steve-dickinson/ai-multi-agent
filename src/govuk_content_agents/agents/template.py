from typing import override
from .base import BaseAgent
from ..templates.govuk_patterns import GOVUK_TEMPLATES

class TemplateAgent(BaseAgent):
    """
    Agent responsible for generating initial content based on a GOV.UK template.
    """
    
    def __init__(self):
        super().__init__(name="Content Architect")

    @override
    def get_system_prompt(self) -> str:
        return """You are the Content Architect for GOV.UK.
Your goal is to scaffold a draft piece of content based on a specific template and user brief.

You MUST return a JSON object with the following fields:
- "summary": A brief explanation of how you approached the draft.
- "rewritten_content": The full markdown content of the draft.
- "score": 100 (always).
- "issues": [] (empty).

The "rewritten_content" must strictly follow the requested structure provided in the user prompt.
Do not invent facts if the brief is vague—use placeholders like [Insert Date].
"""

    async def generate_draft(self, template_key: str, user_brief: str) -> str:
        """
        Generates a draft based on the template key and user brief.
        """
        template = GOVUK_TEMPLATES.get(template_key)
        if not template:
            raise ValueError(f"Unknown template: {template_key}")
            
        # Construct the detailed instructions as the "content" to review/process
        prompt_content = f"""
PLEASE GENERATE CONTENT BASED ON THIS SPECIFICATION:

TEMPLATE NAME: {template['name']}
DESCRIPTION: {template['description']}

SPECIFIC GUIDANCE:
{template['prompt_guidance']}

REQUIRED STRUCTURE (Markdown):
{template['structure']}

---
USER BRIEF:
{user_brief}
"""
        
        # Execute using standard BaseAgent flow
        feedback = await self.execute(prompt_content)
        
        # Return the generated content
        if feedback.rewritten_content:
            return feedback.rewritten_content
            
        return feedback.summary # Fallback if something went wrong
