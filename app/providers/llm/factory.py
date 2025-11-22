"""Factory for creating LLM providers."""

from typing import Optional

from app.providers.llm.base import BaseLLMProvider
from app.providers.llm.openai_provider import OpenAICompatibleProvider, FallbackProvider
from app.core.enums import LLMProvider
from app.core.constants.messages import ErrorMessages, WarningMessages
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_llm_provider(
    provider_type: str,
    model_name: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    max_tokens: int = 1000,
    temperature: float = 0.7,
) -> BaseLLMProvider:
    """Factory function to create the appropriate LLM provider.
    
    Args:
        provider_type: Type of LLM provider (openai, groq, etc.)
        model_name: Name of the model to use
        api_key: API key for the provider
        base_url: Base URL for the API (optional)
        max_tokens: Maximum tokens to generate
        temperature: Temperature for generation
        
    Returns:
        An instance of BaseLLMProvider
    """
    provider_type_lower = provider_type.lower()
    
    # OpenAI provider
    if provider_type_lower == LLMProvider.OPENAI.value:
        url = base_url or "https://api.openai.com/v1/chat/completions"
        return OpenAICompatibleProvider(
            model_name=model_name,
            api_key=api_key,
            base_url=url,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    
    # Groq provider (OpenAI-compatible)
    elif provider_type_lower == LLMProvider.GROQ.value:
        url = base_url or "https://api.groq.com/openai/v1"
        return OpenAICompatibleProvider(
            model_name=model_name,
            api_key=api_key,
            base_url=url,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    
    # Local provider (not yet implemented)
    elif provider_type_lower == LLMProvider.LOCAL.value:
        logger.warning(ErrorMessages.LLM_LOCAL_NOT_IMPLEMENTED)
        return FallbackProvider()
    
    # Fallback provider
    elif provider_type_lower == LLMProvider.FALLBACK.value:
        return FallbackProvider()
    
    # Unknown provider - use fallback
    else:
        logger.warning(ErrorMessages.LLM_PROVIDER_UNKNOWN.format(provider=provider_type))
        return FallbackProvider()

