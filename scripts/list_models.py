import asyncio
import os
import sys
from google import genai

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), "src"))
from govuk_content_agents.config import settings

def main():
    print("Listing available models for your API key...")
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        # Note: In google-genai SDK, list_models might be paginated or different
        # We try the standard way for the new SDK
        
        # Verify if models methods exist or we fall back to manual check
        if hasattr(client, "models") and hasattr(client.models, "list"):
             for m in client.models.list():
                 print(f"- {m.name}")
        else:
            print("Check SDK documentation for list_models. Trying naive verify...")
            
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    main()
