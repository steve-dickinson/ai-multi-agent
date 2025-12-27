from abc import ABC, abstractmethod
from typing import override
import json
import logging
from google import genai
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, InternalServerError

from ..config import settings
from ..storage.models import AgentFeedback

logger = logging.getLogger(__name__)

type Context = dict[str, Any] | None

class BaseAgent(ABC):
    """Abstract base class for all content agents."""
    
    def __init__(self, name: str, model: str = "gpt-4.1-mini"):
        self.name = name
        self.model = model
        
        if self.model.startswith("gpt"):
            self.provider = "openai"
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.provider = "gemini"
            if settings.GEMINI_API_KEY:
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            else:
                self.client = None
                logger.warning("Gemini API key not found, but Gemini model selected.")
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass
        
    async def execute(self, content: str, context: Context = None) -> AgentFeedback:
        """
        Execute the agent on the given content.
        """
        if self.provider == "openai":
            return await self._execute_openai(content, context)
        else:
            return await self._execute_gemini(content, context)

    async def _execute_openai(self, content: str, context: Context = None) -> AgentFeedback:
        system_prompt = self.get_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please review the following content:\n\n{content}"}
        ]
        
        if context:
            messages.append({"role": "user", "content": f"Additional Context:\n{json.dumps(context, indent=2)}"})
            
        try:
            logger.info(f"Agent {self.name} starting execution (OpenAI: {self.model})")
            
            # OpenAI call (using synchronous client in async wrapper if needed, but for now direct call)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            response_text = response.choices[0].message.content
            
            parsed_response = self._parse_response(response_text)
            
            return AgentFeedback(
                agent_name=self.name,
                summary=parsed_response.get("summary", "No summary provided"),
                issues=parsed_response.get("issues", []),
                score=parsed_response.get("score"),
                rewritten_content=parsed_response.get("rewritten_content")
            )
        except Exception as e:
            logger.error(f"Error in agent {self.name} (OpenAI): {e}")
            raise

    @retry(
        retry=retry_if_exception_type((ResourceExhausted, ServiceUnavailable, InternalServerError)),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=10, max=120),
        reraise=True
    )
    async def _execute_gemini(self, content: str, context: Context = None) -> AgentFeedback:
        if not self.client:
             raise ValueError("Gemini API key not configured.")

        system_prompt = self.get_system_prompt()
        prompt = f"{system_prompt}\n\nPlease review the following content:\n\n{content}"
        
        if context:
            prompt += f"\n\nAdditional Context:\n{json.dumps(context, indent=2)}"
            
        try:
            logger.info(f"Agent {self.name} starting execution (Gemini: {self.model})")
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            response_text = response.text
            
            parsed_response = self._parse_response(response_text)
            
            return AgentFeedback(
                agent_name=self.name,
                summary=parsed_response.get("summary", "No summary provided"),
                issues=parsed_response.get("issues", []),
                score=parsed_response.get("score"),
                rewritten_content=parsed_response.get("rewritten_content")
            )
        except Exception as e:
            logger.error(f"Error in agent {self.name} (Gemini): {e}")
            raise

    async def get_embedding(self, text: str) -> list[float]:
        """Generate embedding for text."""
        try:
            if self.provider == "openai":
                response = self.client.embeddings.create(
                    input=text,
                    model="text-embedding-3-small"
                )
                return response.data[0].embedding
            else:
                if settings.OPENAI_API_KEY:
                   client = OpenAI(api_key=settings.OPENAI_API_KEY)
                   response = client.embeddings.create(input=text, model="text-embedding-3-small")
                   return response.data[0].embedding
                else:
                    raise ValueError("OpenAI API Key required for vector search (1536 dimensions).")
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def _parse_response(self, text: str) -> dict[str, Any]:
        """Parse JSON response from LLM."""
        try:
            # Clean up potential markdown formatting
            text = text.replace("```json", "").replace("```", "").strip()
            
            # Find JSON/dict structure if wrapped
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = text[start:end]
                return json.loads(json_str)
            return {"summary": text, "issues": []}
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON response from {self.name}")
            return {"summary": text, "issues": []}
