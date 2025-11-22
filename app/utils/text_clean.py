import re
from typing import List
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s.,!?;:\-\(\)\'\"]+", "", text)
    text = re.sub(r"http[s]?://\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = text.strip()
    return text


def chunk_text(
    text: str, chunk_size: int = None, chunk_overlap: int = None
) -> List[str]:
    if not text:
        return []
    chunk_size = chunk_size or settings.CHUNK_SIZE
    chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
    text = clean_text(text)
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if end < len(text):
            last_period = max(chunk.rfind("."), chunk.rfind("!"), chunk.rfind("?"))
            if last_period > chunk_size * 0.8:
                chunk = chunk[: last_period + 1]
                end = start + last_period + 1
        chunks.append(chunk.strip())
        start = end - chunk_overlap
        if start <= 0 and len(chunks) > 0:
            break
    logger.debug(f"Split text into {len(chunks)} chunks")
    return chunks


def extract_sentences(text: str) -> List[str]:
    text = clean_text(text)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def truncate_text(text: str, max_length: int = 1000) -> str:
    if len(text) <= max_length:
        return text
    truncated = text[:max_length]
    last_period = max(truncated.rfind("."), truncated.rfind("!"), truncated.rfind("?"))
    if last_period > max_length * 0.7:
        return truncated[: last_period + 1]
    return truncated + "..."
