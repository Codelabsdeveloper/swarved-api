from enum import Enum

class LLMProvider(str, Enum):
    OPENAI = "openai"
    GROQ = "groq"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    FALLBACK = "fallback"


class EmbeddingProvider(str, Enum):
    SENTENCE_TRANSFORMERS = "sentence-transformers"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"