import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Swarved RAG Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    DOCUMENTS_DIR: Path = DATA_DIR / "documents"
    PROCESSED_DIR: Path = DATA_DIR / "processed"
    VECTOR_STORE_DIR: Path = DATA_DIR / "vector_store"

    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    EMBEDDING_DEVICE: str = "cpu"

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    MAX_DOCUMENT_SIZE_MB: int = 50

    VECTOR_DB_TYPE: str = "chromadb"
    CHROMA_COLLECTION_NAME: str = "swarved_documents"
    CHROMA_PERSIST_DIR: Path = VECTOR_STORE_DIR

    TOP_K_RETRIEVAL: int = 5
    SIMILARITY_THRESHOLD: float = 0.3

    LLM_PROVIDER: str = "groq"
    LLM_MODEL_NAME: str = "llama-3.1-70b-versatile"
    LLM_API_KEY: Optional[str] = None
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    LLM_MAX_TOKENS: int = 1000
    LLM_TEMPERATURE: float = 0.7

    SUPPORTED_LANGUAGES: list = ["en", "hi", "es", "fr", "de"]
    DEFAULT_LANGUAGE: str = "en"
    
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()

settings.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
settings.VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)