import sys
import os

# Add src to path just like app.py
sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from govuk_content_agents.utils.web import fetch_content_from_govuk_api
    print("✅ Import successful!")
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
