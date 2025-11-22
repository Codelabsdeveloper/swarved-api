"""Message constants for errors, success, and info messages."""


class ErrorMessages:
    """Error message constants."""
    
    # LLM errors
    LLM_NOT_CONFIGURED = "LLM is not configured. Please provide an API key."
    LLM_API_ERROR = "Error generating answer: {error}"
    LLM_PROVIDER_UNKNOWN = "Unknown LLM provider: {provider}"
    LLM_LOCAL_NOT_IMPLEMENTED = "Local LLM integration coming soon."
    
    # Embedding errors
    EMBEDDING_LOAD_FAILED = "Failed to load embedding model: {error}"
    EMBEDDING_GENERATION_FAILED = "Error generating embeddings: {error}"
    EMBEDDING_EMPTY_INPUT = "Empty input to embed()"
    
    # Document errors
    DOCUMENT_NOT_FOUND = "File not found: {path}"
    DOCUMENT_TOO_LARGE = "File too large: {size}MB > {max_size}MB"
    DOCUMENT_TEXT_EXTRACTION_FAILED = "Failed to extract text from document"
    DOCUMENT_NO_CHUNKS = "No chunks created from document"
    DOCUMENT_UNSUPPORTED_TYPE = "Unsupported file type: {extension}"
    
    # Vector DB errors
    VECTOR_DB_ADD_FAILED = "Error adding vectors to FAISS: {error}"
    VECTOR_DB_SEARCH_FAILED = "Error searching vectors in FAISS: {error}"
    VECTOR_DB_DELETE_FAILED = "Error deleting vectors from FAISS: {error}"
    VECTOR_DB_LOAD_FAILED = "Error loading/creating FAISS index: {error}"
    VECTOR_DB_SAVE_FAILED = "Error saving FAISS index: {error}"
    VECTOR_DB_EMPTY = "FAISS index is empty"
    VECTOR_DB_COUNT_FAILED = "Error counting documents in FAISS: {error}"
    VECTOR_DB_HEALTH_CHECK_FAILED = "FAISS health check failed: {error}"
    VECTOR_DB_RESET_FAILED = "Error resetting FAISS index: {error}"
    
    # File reading errors
    FILE_READ_TEXT_FAILED = "Error reading text file {path}: {error}"
    FILE_READ_PDF_FAILED = "Error reading PDF file {path}: {error}"
    FILE_READ_DOC_FAILED = "Error reading DOC file {path}: {error}"
    FILE_READ_DOCX_FAILED = "Error reading DOCX file {path}: {error}"
    
    # PyPDF2 not installed
    PYPDF2_NOT_INSTALLED = "PyPDF2 not installed. Install with: pip install PyPDF2"
    ANTIWORD_NOT_INSTALLED = "antiword not installed. Install with: brew install antiword"
    ANTIWORD_FAILED = "antiword failed for {path}"
    
    # RAG pipeline errors
    RAG_PIPELINE_ERROR = "Error in RAG pipeline: {error}"
    RAG_RETRIEVAL_ERROR = "Error in retrieval: {error}"
    RAG_INITIALIZATION_FAILED = "Failed to initialize RAG pipeline: {error}"
    
    # Ingestion errors
    INGESTION_ERROR = "Error ingesting document: {error}"
    INVALID_DIRECTORY = "Invalid directory: {path}"
    
    # Translation errors
    TRANSLATION_ERROR = "Error detecting language: {error}"
    UNSUPPORTED_LANGUAGE = "Unsupported language: {language}"
    
    # General errors
    INTERNAL_SERVER_ERROR = "Internal server error"
    UNHANDLED_EXCEPTION = "Unhandled exception: {error}"
    QUERY_PROCESSING_ERROR = "Error processing query: {error}"
    VECTORS_PAYLOADS_MISMATCH = "Number of vectors and payloads must match"


class SuccessMessages:
    """Success message constants."""
    
    # LLM success
    LLM_ANSWER_GENERATED = "Successfully generated answer using {provider}"
    
    # Embedding success
    EMBEDDING_MODEL_LOADED = "Embedding model loaded successfully on {device}"
    EMBEDDINGS_GENERATED = "Generated embeddings for {count} texts"
    
    # Document success
    DOCUMENT_INGESTED = "Successfully ingested document {name}"
    DOCUMENTS_INGESTED = "Successfully ingested {success}/{total} documents"
    
    # Vector DB success
    VECTORS_ADDED = "Added {count} vectors to FAISS index"
    VECTORS_FOUND = "Found {count} similar vectors in FAISS"
    VECTORS_DELETED = "Deleted vectors for document: {document_id}"
    
    # RAG pipeline success
    RAG_ANSWER_GENERATED = "Successfully generated answer"
    RAG_CHUNKS_RETRIEVED = "Retrieved {count} relevant chunks"
    RAG_PIPELINE_INITIALIZED = "RAG pipeline initialized successfully"
    
    # General success
    SERVER_STARTED = "Starting {name} server"


class InfoMessages:
    """Info message constants."""
    
    # LLM info
    LLM_FALLBACK_RESPONSE = "Using fallback response (no LLM)"
    
    # Embedding info
    EMBEDDING_MODEL_LOADING = "Loading embedding model: {model}"
    
    # Document info
    DOCUMENT_READING = "Reading document: {name}"
    DOCUMENT_INGESTING = "Ingesting document: {name} ({size}MB)"
    DOCUMENTS_FOUND = "Found {count} documents to ingest"
    TEXT_EXTRACTED = "Extracted {count} characters"
    CHUNKS_CREATED = "Created {count} chunks"
    
    # Vector DB info
    FAISS_LOADING = "Loading existing FAISS index from: {path}"
    FAISS_LOADED = "Loaded FAISS index with {count} vectors"
    FAISS_CREATING = "Creating new FAISS index"
    FAISS_CREATED = "New FAISS index created"
    FAISS_REBUILDING = "Rebuilding FAISS index after deleting document: {document_id}"
    
    # RAG pipeline info
    QUERY_PROCESSING = "Processing query: {query}"
    QUERY_RECEIVED = "Received query: {query}"
    
    # Translation info
    TRANSLATION_REQUESTED = "Translation requested: {source} -> {target}"
    TRANSLATION_NOT_IMPLEMENTED = "Translation not implemented yet, returning original text"
    LANGUAGE_DETECTED = "Detected language: {language}"
    
    # General info
    SERVER_CONFIG = "Host: {host}, Port: {port}, Debug: {debug}"
    APP_STARTING = "Starting {name} v{version}"
    
    # No results
    NO_RELEVANT_DOCUMENTS = "The provided documents do not contain this information."
    NO_DOCUMENT_VECTORS_FOUND = "No vectors found for document: {document_id}"


class WarningMessages:
    """Warning message constants."""
    
    FAISS_DELETION_REBUILD_REQUIRED = "FAISS deletion requires rebuilding. Consider re-ingesting documents."
    FAISS_INDEX_RESET = "FAISS index has been reset"

