from typing import List, Optional, Dict, Any
import requests
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLMModel:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model_name = settings.LLM_MODEL_NAME
        self.api_key = settings.LLM_API_KEY
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.temperature = settings.LLM_TEMPERATURE

    def generate(
        self,
        prompt: str,
        context: List[str],
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        full_prompt = self._build_prompt(prompt, context, history)

        if self.provider == "openai":
            return self._generate_openai(full_prompt)
        elif self.provider == "local":
            return self._generate_local(full_prompt)
        else:
            logger.warning(f"Unknown LLM provider: {self.provider}, using fallback")
            return self._generate_fallback(context)

    def _build_prompt(
        self,
        query: str,
        context: List[str],
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        system_prompt = (
            "You are Swarved, an AI assistant that answers questions using only the information from provided documents.\n\n"
            "Rules:\n"
            "1. Only use information from the context below\n"
            '2. If the answer is not in the context, say: "The provided documents do not contain this information."\n'
            "3. Be concise, clear, and structured\n"
            "4. Never invent or hallucinate information\n"
            "5. Cite sources when possible\n"
            "6. Maintain conversational continuity"
        )
        context_text = "\n\n".join(
            [f"[Document {i+1}]\n{ctx}" for i, ctx in enumerate(context)]
        )
        history_text = ""
        if history:
            history_text = "\n".join(
                [f"{msg['role'].capitalize()}: {msg['content']}" for msg in history]
            )
            history_text = f"\n\nConversation History:\n{history_text}\n"
        full_prompt = f"""{system_prompt}

Context from documents:
{context_text}
{history_text}

User Question: {query}

Answer:"""
        return full_prompt

    def _generate_openai(self, prompt: str) -> str:
        if not self.api_key:
            logger.error("OpenAI API key not configured")
            return "LLM is not configured. Please provide an API key."
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            logger.info("Successfully generated answer using OpenAI")
            return answer.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Error generating answer: {str(e)}"

    def _generate_local(self, prompt: str) -> str:
        logger.warning("Local LLM not implemented yet")
        return "Local LLM integration coming soon."

    def _generate_fallback(self, context: List[str]) -> str:
        if not context:
            return "The provided documents do not contain this information."
        logger.info("Using fallback response (no LLM)")
        return f"Based on the documents:\n\n{context[0]}"


_llm_instance = None


def get_llm_model() -> LLMModel:
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LLMModel()
    return _llm_instance
