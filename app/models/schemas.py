from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class Message(BaseModel):
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class QueryRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User's question")
    history: List[Message] = Field(default_factory=list, description="Conversation history")
    language: Optional[str] = Field(default="en", description="Response language")
    top_k: Optional[int] = Field(
        default=5, ge=1, le=20, description="Number of chunks to retrieve"
    )


class Source(BaseModel):
    document_name: str = Field(..., description="Name of source document")
    content: str = Field(..., description="Relevant text chunk")
    score: float = Field(..., description="Similarity score")
    page: Optional[int] = Field(default=None, description="Page number if available")


class QueryResponse(BaseModel):
    answer: str = Field(..., description="Generated answer")
    sources: List[Source] = Field(default_factory=list, description="Source documents used")
    language: str = Field(default="en", description="Language of response")
    confidence: Optional[float] = Field(
        default=None, description="Answer confidence score"
    )


class DocumentUploadResponse(BaseModel):
    status: str = Field(..., description="Status: success or error")
    message: str = Field(..., description="Human-readable message")
    document_id: Optional[str] = Field(default=None, description="Unique document ID")
    chunks_created: Optional[int] = Field(
        default=None, description="Number of chunks created"
    )


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    qdrant_connected: bool = Field(..., description="Qdrant connection status")
    documents_indexed: int = Field(..., description="Number of documents in index")


class Chunk(BaseModel):
    text: str = Field(..., description="Chunk text content")
    chunk_id: str = Field(..., description="Unique chunk identifier")
    document_id: str = Field(..., description="Parent document ID")
    document_name: str = Field(..., description="Source document name")
    page: Optional[int] = Field(default=None, description="Page number")
    chunk_index: int = Field(..., description="Index within document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
