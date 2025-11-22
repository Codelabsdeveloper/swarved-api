"""API-related constants including URLs, endpoints, and HTTP settings."""


class APIConstants:
    """API configuration constants."""
    
    # OpenAI API
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_API_TIMEOUT = 30
    
    # Groq API (uses OpenAI-compatible endpoint)
    GROQ_API_URL = "https://api.groq.com/openai/v1"
    GROQ_API_TIMEOUT = 30
    
    # HTTP Headers
    HEADER_CONTENT_TYPE = "Content-Type"
    HEADER_AUTHORIZATION = "Authorization"
    CONTENT_TYPE_JSON = "application/json"
    
    # CORS
    CORS_ALLOW_ORIGINS = ["*"]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]
    
    # API Tags
    TAG_SYSTEM = "System"
    TAG_RAG = "RAG"
    TAG_DOCUMENTS = "Documents"
    
    # Endpoints
    ENDPOINT_ROOT = "/"
    ENDPOINT_HEALTH = "/health"
    ENDPOINT_QUERY = "/query"
    ENDPOINT_DOCS = "/docs"
    
    # Response Messages
    API_RUNNING_STATUS = "running"
    API_DESCRIPTION = "RAG Backend for Document Question Answering"

