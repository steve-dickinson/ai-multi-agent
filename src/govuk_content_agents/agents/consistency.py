from typing import Dict, Any, Optional
from .base import BaseAgent
from ..storage.vectors import vector_client, VectorDBClient

class ConsistencyAgent(BaseAgent):
    """
    Agent responsible for checking content consistency.
    Uses vector search to find duplicates or contradictory content in the database.
    """
    
    def __init__(self):
        super().__init__(name="Consistency Checker")
        # Ensure we have vector client
        self.vector_db = vector_client

    def get_system_prompt(self) -> str:
        return """You are a Consistency Checker for GOV.UK content.
Your role is to ensure the new content does not duplicate or contradict existing content.

You will be provided with "Existing Similar Content" found in our knowledge base.
Some content comes from OTHER DEPARTMENTS (e.g., HMRC, DWP).

Analyze for:
1.  **Duplication**: Is this content already published?
2.  **Contradiction (CRITICAL)**: Does this content violate a policy from another department? 
    *   Example: If the text says "VAT is optional" but HMRC says "VAT is mandatory", this is a HIGH SEVERITY ERROR.
3.  **Related Links**: Suggest existing content that should be linked to.

Output JSON:
{
  "summary": "Analysis of consistency with existing content",
  "score": 0-100 (100 = unique and consistent, 0 = exact duplicate or policy violation),
  "issues": [
    {
      "severity": "High|Medium|Low",
      "description": "Description of conflict or duplication. Mention the Department if applicable.",
      "suggestion": "Link to existing page X instead / Update existing page X"
    }
  ]
}
"""

    async def execute(self, content: str, context: Optional[Dict[str, Any]] = None) -> Any:
        # 1. Generate embedding for new content
        embedding = await self.get_embedding(content)
        
        # 2. Search for similar content
        similar_items = self.vector_db.search_similar(embedding, limit=3)
        
        # 3. Format context for LLM
        db_context = "No existing content found."
        if similar_items:
            db_context = "Found the following similar content in database:\n"
            for item in similar_items:
                similarity = item.get('similarity', 0)
                # Only include relevant matches
                if similarity > 0.7:
                    db_context += f"- [ID: {item['id']}] (Similarity: {similarity:.2f}): {item['content'][:200]}...\n"
        
        # 4. Pass combined context to LLM
        full_context = {"existing_content": db_context}
        if context:
            full_context.update(context)
            
        return await super().execute(content, context=full_context)
