"""Base class for LLM providers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ):
        self.model_name = model_name
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.temperature = temperature
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        context: List[str],
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """Generate a response using the LLM.
        
        Args:
            prompt: The user's query
            context: Retrieved context from documents
            history: Conversation history
            
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    def _call_api(self, messages: List[Dict[str, str]]) -> str:
        """Call the LLM API with formatted messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Generated response text
        """
        pass
    
    def is_configured(self) -> bool:
        """Check if the provider is properly configured."""
        return self.api_key is not None

