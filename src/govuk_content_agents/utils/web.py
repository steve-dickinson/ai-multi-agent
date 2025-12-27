import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def fetch_content_from_url(url: str) -> str:
    """
    Fetch and extract main text content from a URL.
    Returns the text content or raises an exception.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        logger.error(f"Error fetching URL {url}: {e}")
        raise ValueError(f"Could not fetch content from URL: {e}")

def fetch_content_from_govuk_api(url_or_path: str) -> str:
    """
    Fetch content from GOV.UK Content API.
    Input can be a full URL (https://www.gov.uk/x) or path (/x).
    """
    try:
        # Normalize input to path
        path = url_or_path
        if "gov.uk" in path:
            from urllib.parse import urlparse
            path = urlparse(path).path
            
        api_url = f"https://www.gov.uk/api/content{path}"
        
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract fields
        title = data.get("title", "")
        description = data.get("description", "")
        details = data.get("details", {})
        
        content_parts = []
        
        # 1. Main Body
        body_html = details.get("body", "")
        if body_html:
             soup = BeautifulSoup(body_html, 'html.parser')
             content_parts.append(soup.get_text(separator="\n").strip())

        # 2. Parts (for guides)
        parts = details.get("parts", [])
        if parts:
            for part in parts:
                part_title = part.get("title", "")
                part_body_html = part.get("body", "")
                if part_title:
                    content_parts.append(f"\n--- Part: {part_title} ---")
                if part_body_html:
                    soup = BeautifulSoup(part_body_html, 'html.parser')
                    content_parts.append(soup.get_text(separator="\n").strip())
                    
        # Combine
        full_body = "\n\n".join(content_parts)
        full_content = f"Title: {title}\n\nDescription: {description}\n\n{full_body}"
        return full_content.strip()
        
    except Exception as e:
        logger.error(f"Error fetching from GOV.UK API: {e}")
        raise ValueError(f"Could not fetch content from GOV.UK API: {e}")
