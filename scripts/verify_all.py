
import asyncio
import sys
import os

sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.agents.content_reviewer import ContentReviewerAgent
from govuk_content_agents.agents.style_compliance import StyleComplianceAgent
from govuk_content_agents.agents.consistency import ConsistencyAgent
from govuk_content_agents.agents.improvement import ImprovementAgent
from govuk_content_agents.agents.persona import PersonaAgent
from govuk_content_agents.agents.debate import SimplifierAgent, LegalistAgent

async def main():
    print("Verifying imports...")
    
    agents = [
        ContentReviewerAgent(),
        StyleComplianceAgent(),
        ConsistencyAgent(),
        ImprovementAgent(),
        PersonaAgent(),
        SimplifierAgent(),
        LegalistAgent()
    ]
    
    print(f"Successfully instantiated {len(agents)} agents.")
    
    print("Verifying basic execution (dry run)...")
    # We won't actually call the LLM to save time/cost, just checking methods exist
    for agent in agents:
        assert hasattr(agent, 'execute'), f"{agent.name} missing execute method"
        assert hasattr(agent, 'get_system_prompt'), f"{agent.name} missing system prompt"
        print(f" - {agent.name}: OK")
        
    print("All checks passed!")

if __name__ == "__main__":
    asyncio.run(main())
