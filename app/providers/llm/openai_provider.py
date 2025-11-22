"""OpenAI-compatible LLM provider (supports OpenAI, Groq, etc.)."""

from typing import List, Dict, Optional
import requests

from app.providers.llm.base import BaseLLMProvider
from app.core.prompts import RAGPrompts
from app.core.constants.messages import ErrorMessages, SuccessMessages, InfoMessages
from app.core.constants.api import APIConstants
from app.core.exceptions import LLMException
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OpenAICompatibleProvider(BaseLLMProvider):
    """OpenAI-compatible LLM provider supporting OpenAI, Groq, and similar APIs."""
    
    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        base_url: str = APIConstants.OPENAI_API_URL,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        timeout: int = APIConstants.OPENAI_API_TIMEOUT,
    ):
        super().__init__(model_name, api_key, max_tokens, temperature)
        self.base_url = base_url
        self.timeout = timeout
    
    def generate(
        self,
        prompt: str,
        context: List[str],
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Generate a response using OpenAI-compatible API."""
        if not self.is_configured():
            logger.error(ErrorMessages.LLM_NOT_CONFIGURED)
            return ErrorMessages.LLM_NOT_CONFIGURED
        
        try:
            # Build the full prompt
            full_prompt = RAGPrompts.build_full_prompt(prompt, context, history)
            
            # Format as messages for the API
            messages = [{"role": "user", "content": full_prompt}]
            
            # Call the API
            answer = self._call_api(messages)
            
            logger.info(SuccessMessages.LLM_ANSWER_GENERATED.format(provider=self.model_name))
            return answer.strip()
            
        except LLMException as e:
            logger.error(f"{ErrorMessages.LLM_API_ERROR.format(error=str(e))}")
            return ErrorMessages.LLM_API_ERROR.format(error=str(e))
        except Exception as e:
            logger.error(f"{ErrorMessages.LLM_API_ERROR.format(error=str(e))}")
            return ErrorMessages.LLM_API_ERROR.format(error=str(e))
    
    def _call_api(self, messages: List[Dict[str, str]]) -> str:
        """Call the OpenAI-compatible API."""
        try:
            headers = {
                APIConstants.HEADER_AUTHORIZATION: f"Bearer {self.api_key}",
                APIConstants.HEADER_CONTENT_TYPE: APIConstants.CONTENT_TYPE_JSON,
            }
            
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }
            
            # Determine the endpoint
            if self.base_url.endswith("/chat/completions"):
                url = self.base_url
            elif "groq" in self.base_url.lower():
                url = f"{self.base_url}/chat/completions"
            else:
                url = self.base_url
            
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            return answer
            
        except requests.exceptions.RequestException as e:
            raise LLMException(f"API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise LLMException(f"Invalid API response format: {str(e)}")
        except Exception as e:
            raise LLMException(f"Unexpected error: {str(e)}")


class FallbackProvider(BaseLLMProvider):
    """Fallback provider when no LLM is configured."""
    
    def __init__(self):
        super().__init__(model_name="fallback", api_key=None)
    
    def generate(
        self,
        prompt: str,
        context: List[str],
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Return a fallback response."""
        if not context:
            return InfoMessages.NO_RELEVANT_DOCUMENTS
        
        logger.info(InfoMessages.LLM_FALLBACK_RESPONSE)
        return RAGPrompts.FALLBACK_RESPONSE_WITH_CONTEXT.format(context=context[0])
    
    def _call_api(self, messages: List[Dict[str, str]]) -> str:
        """Not implemented for fallback provider."""
        return InfoMessages.NO_RELEVANT_DOCUMENTS
    
    def is_configured(self) -> bool:
        """Fallback is always available."""
        return True

