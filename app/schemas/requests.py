from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.common import Message
from app.core.constants.defaults import DefaultValues


class QueryRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User's question")
    history: List[Message] = Field(default_factory=list, description="Conversation history")
    language: Optional[str] = Field(
        default=DefaultValues.DEFAULT_LANGUAGE,
        description="Response language"
    )
    top_k: Optional[int] = Field(
        default=DefaultValues.DEFAULT_TOP_K,
        ge=DefaultValues.DEFAULT_TOP_K_MIN,
        le=DefaultValues.DEFAULT_TOP_K_MAX,
        description="Number of chunks to retrieve"
    )