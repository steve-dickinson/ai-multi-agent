import asyncio
import sys
import os

# Ensure src is in path for local development if package not installed
sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.storage.mongodb import mongo_client
from govuk_content_agents.storage.vectors import vector_client
from govuk_content_agents.agents.content_reviewer import ContentReviewerAgent

async def check_databases():
    print("Checking database connections...")
    
    # Check MongoDB
    try:
        await mongo_client.connect()
        print("✅ MongoDB connection successful")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

    # Check Postgres
    try:
        vector_client.connect()
        print("✅ PostgreSQL/pgvector connection successful")
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False
        
    return True

async def check_agent():
    print("\nChecking Agent initialization...")
    try:
        agent = ContentReviewerAgent()
        print(f"✅ Agent '{agent.name}' initialized with model '{agent.model}'")
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

async def main():
    print("=== Stage 1 Verification (Gemini) ===\n")
    
    db_ok = await check_databases()
    agent_ok = await check_agent()
    
    print("\n=== Result ===")
    if db_ok and agent_ok:
        print("✅ Stage 1 verification PASSED")
        sys.exit(0)
    else:
        print("❌ Stage 1 verification FAILED")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
