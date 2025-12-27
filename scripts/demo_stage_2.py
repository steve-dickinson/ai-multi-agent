import asyncio
import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.orchestration.graph import app
from govuk_content_agents.config import settings

SAMPLE_CONTENT = """
Subject: Tax Returns

It is imperative that you facilitate the submission of your taxation documentation 
by the appropriate deadline. Failure to do so may result in pecuniary penalties 
being administrated by the authority. 

The mechanism for submission is via the digital portal which can be accessed 
through the internet.
"""

async def main():
    print("=== Stage 2 Demo: Multi-Agent Orchestra ===")
    
    if not settings.OPENAI_API_KEY:
         print("❌ OPENAI_API_KEY required in .env")
         return

    print("Initializing workflow...")
    
    initial_state = {
        "input_content": SAMPLE_CONTENT,
        "current_content": SAMPLE_CONTENT,
        "feedback": [],
        "iteration": 0,
        "max_iterations": 3,
        "metadata": {}
    }
    
    print("\n--- Starting Execution ---")
    async for event in app.astream(initial_state):
        for key, value in event.items():
            print(f"\n[Node: {key}]")
            if key == "judge":
                print(f"  Score: {value.get('final_score')}")
                print(f"  Decision: {value.get('final_decision')}")
            elif key == "improve":
                print(f"  Iteration: {value.get('iteration')}")
                print(f"  Content updated.")
                
    print("\n✅ Workflow Complete!")

if __name__ == "__main__":
    asyncio.run(main())
