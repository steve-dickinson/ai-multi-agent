import asyncio
import os
import sys

# Ensure src is in path
sys.path.append(os.getcwd())

from src.govuk_content_agents.data.external_policies import EXTERNAL_POLICIES
from src.govuk_content_agents.storage.vectors import vector_client
from src.govuk_content_agents.storage.models import ContentEmbedding, generate_uuid
from src.govuk_content_agents.config import settings
from openai import OpenAI
from datetime import datetime

async def seed_policies():
    print("🚀 Seeding External Policies into Vector Store...")
    
    # Initialize OpenAI for embeddings
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    # Connect DB
    vector_client.connect()
    
    for policy in EXTERNAL_POLICIES:
        content = f"{policy['title']}\n\n{policy['content']}"
        print(f"Processing: {policy['title']} ({policy['department']})")
        
        # Generate Embedding
        response = client.embeddings.create(
            input=content,
            model="text-embedding-3-small"
        )
        embedding = response.data[0].embedding
        
        # Create Model
        item = ContentEmbedding(
            id=generate_uuid(),
            content=content,
            embedding=embedding,
            metadata={
                "department": policy["department"],
                "type": "external_policy",
                "title": policy["title"]
            },
            created_at=datetime.utcnow()
        )
        
        # Store in DB (Sync call)
        vector_client.save_embedding(item)
        
    print("✅ Seeding Complete!")
    vector_client.close()

if __name__ == "__main__":
    asyncio.run(seed_policies())
