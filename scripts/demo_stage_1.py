import asyncio
import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.agents.content_reviewer import ContentReviewerAgent
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
    print("=== Stage 1 Demo: Content Reviewer Agent ===")
    
    # Check for OpenAI key
    if "dummy" in settings.OPENAI_API_KEY:
         print("\n⚠️  WARNING: It looks like you are using a dummy OpenAI API key.")
         print("Please edit your .env file with a valid OPENAI_API_KEY.")
    
    # Initialize agent (defaults to gpt-4o-mini)
    agent = ContentReviewerAgent()
    print(f"Using Provider: {agent.provider.upper()}")
    print(f"Using Model: {agent.model}")
    
    print(f"\nAnalyzing sample content:\n---\n{SAMPLE_CONTENT}\n---")
    print("Running agent... (this should be fast)")
    
    try:
        result = await agent.execute(SAMPLE_CONTENT)
        
        print("\n✅ Analysis Complete!")
        print(f"\nSummary: {result.summary}")
        print(f"Score: {result.score}")
        print("\nIssues Found:")
        for issue in result.issues:
            print(f"- [{issue.get('severity', 'medium').upper()}] {issue.get('description')}")
            print(f"  Suggestion: {issue.get('suggestion')}")
            
    except Exception as e:
        print(f"\n❌ Error running agent: {e}")
        if "api_key" in str(e).lower() or "401" in str(e):
             print("\nTip: Check your OPENAI_API_KEY in the .env file.")

if __name__ == "__main__":
    asyncio.run(main())
