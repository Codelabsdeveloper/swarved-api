
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import LLMProvider, Language
from app.core.constants.defaults import DefaultValues


class Settings(BaseSettings):
    
    # Application info
    APP_NAME: str = "Swarved RAG Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server settings
    HOST: str = DefaultValues.DEFAULT_HOST
    PORT: int = DefaultValues.DEFAULT_PORT

    # Directory paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    DOCUMENTS_DIR: Path = DATA_DIR / "documents"
    PROCESSED_DIR: Path = DATA_DIR / "processed"
    VECTOR_STORE_DIR: Path = DATA_DIR / "vector_store"

    # Embedding model settings
    EMBEDDING_MODEL_NAME: str = DefaultValues.DEFAULT_EMBEDDING_MODEL
    EMBEDDING_DIMENSION: int = DefaultValues.DEFAULT_EMBEDDING_DIMENSION
    EMBEDDING_DEVICE: str = DefaultValues.DEFAULT_EMBEDDING_DEVICE

    # Text chunking settings
    CHUNK_SIZE: int = DefaultValues.DEFAULT_CHUNK_SIZE
    CHUNK_OVERLAP: int = DefaultValues.DEFAULT_CHUNK_OVERLAP
    MAX_DOCUMENT_SIZE_MB: int = DefaultValues.DEFAULT_MAX_DOCUMENT_SIZE_MB

    # Vector database settings
    VECTOR_DB_TYPE: str = "chromadb"
    CHROMA_COLLECTION_NAME: str = "swarved_documents"
    CHROMA_PERSIST_DIR: Path = VECTOR_STORE_DIR

    # Retrieval settings
    TOP_K_RETRIEVAL: int = DefaultValues.DEFAULT_TOP_K
    SIMILARITY_THRESHOLD: float = DefaultValues.DEFAULT_SIMILARITY_THRESHOLD

    # LLM settings
    LLM_PROVIDER: str = DefaultValues.DEFAULT_LLM_PROVIDER
    LLM_MODEL_NAME: str = DefaultValues.DEFAULT_LLM_MODEL
    LLM_API_KEY: Optional[str] = None
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    LLM_MAX_TOKENS: int = DefaultValues.DEFAULT_MAX_TOKENS
    LLM_TEMPERATURE: float = DefaultValues.DEFAULT_TEMPERATURE

    # Language settings
    SUPPORTED_LANGUAGES: list = [lang.value for lang in Language]
    DEFAULT_LANGUAGE: str = DefaultValues.DEFAULT_LANGUAGE
    
    # Logging settings
    LOG_LEVEL: str = DefaultValues.DEFAULT_LOG_LEVEL

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()

settings.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
settings.VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)