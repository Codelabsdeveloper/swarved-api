"""Default values for various configurations."""


class DefaultValues:
    """Default configuration values."""
    
    # Chunking defaults
    DEFAULT_CHUNK_SIZE = 500
    DEFAULT_CHUNK_OVERLAP = 100
    DEFAULT_CHUNK_SENTENCE_BOUNDARY_RATIO = 0.8
    
    # Retrieval defaults
    DEFAULT_TOP_K = 5
    DEFAULT_SIMILARITY_THRESHOLD = 0.3
    DEFAULT_TOP_K_MIN = 1
    DEFAULT_TOP_K_MAX = 20
    
    # LLM defaults
    DEFAULT_MAX_TOKENS = 1000
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_LLM_PROVIDER = "groq"
    DEFAULT_LLM_MODEL = "llama-3.1-70b-versatile"
    
    # Embedding defaults
    DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    DEFAULT_EMBEDDING_DIMENSION = 384
    DEFAULT_EMBEDDING_DEVICE = "cpu"
    
    # Language defaults
    DEFAULT_LANGUAGE = "en"
    
    # Document defaults
    DEFAULT_MAX_DOCUMENT_SIZE_MB = 50
    DEFAULT_SUPPORTED_EXTENSIONS = [".txt", ".pdf", ".docx", ".doc"]
    
    # Text processing defaults
    DEFAULT_TRUNCATE_LENGTH = 1000
    DEFAULT_TRUNCATE_SENTENCE_RATIO = 0.7
    DEFAULT_SOURCE_PREVIEW_LENGTH = 200
    
    # Server defaults
    DEFAULT_HOST = "0.0.0.0"
    DEFAULT_PORT = 8000
    DEFAULT_LOG_LEVEL = "INFO"
    
    # Search multiplier for filtering
    SEARCH_K_MULTIPLIER = 3

