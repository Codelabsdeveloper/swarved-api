from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class Source(BaseModel):
    document_name: str = Field(..., description="Name of source document")
    content: str = Field(..., description="Relevant text chunk")
    score: float = Field(..., description="Similarity score")
    page: Optional[int] = Field(default=None, description="Page number if available")


class Chunk(BaseModel):
    text: str = Field(..., description="Chunk text content")
    chunk_id: str = Field(..., description="Unique chunk identifier")
    document_id: str = Field(..., description="Parent document ID")
    document_name: str = Field(..., description="Source document name")
    page: Optional[int] = Field(default=None, description="Page number")
    chunk_index: int = Field(..., description="Index within document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")