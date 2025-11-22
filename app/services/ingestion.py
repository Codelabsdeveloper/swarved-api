from pathlib import Path
from typing import List, Optional
import uuid
from app.config import settings
from app.utils.logger import get_logger
from app.utils.pdf_reader import read_document, get_file_size_mb
from app.utils.text_clean import chunk_text
from app.models.embedding import get_embedding_model
from app.services.vector_db import get_vector_db
from app.models.schemas import Chunk

logger = get_logger(__name__)


class IngestionService:

    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.vector_db = get_vector_db()

    def ingest_document(self, file_path: Path) -> Optional[dict]:
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return None

            file_size_mb = get_file_size_mb(file_path)
            if file_size_mb > settings.MAX_DOCUMENT_SIZE_MB:
                logger.error(
                    f"File too large: {file_size_mb}MB > {settings.MAX_DOCUMENT_SIZE_MB}MB"
                )
                return None

            logger.info(f"Ingesting document: {file_path.name} ({file_size_mb}MB)")

            text = read_document(file_path)
            if not text:
                logger.error("Failed to extract text from document")
                return None

            logger.info(f"Extracted {len(text)} characters")

            chunks = chunk_text(text)
            if not chunks:
                logger.error("No chunks created from document")
                return None

            logger.info(f"Created {len(chunks)} chunks")

            embeddings = self.embedding_model.embed_documents(chunks)

            document_id = str(uuid.uuid4())
            payloads = []

            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                payload = {
                    "document_id": document_id,
                    "document_name": file_path.name,
                    "chunk_index": idx,
                    "text": chunk,
                    "chunk_id": f"{document_id}_{idx}",
                }
                payloads.append(payload)

            point_ids = self.vector_db.add_vectors(
                vectors=embeddings.tolist(), payloads=payloads
            )

            logger.info(f"Successfully ingested document {file_path.name}")

            return {
                "document_id": document_id,
                "document_name": file_path.name,
                "chunks_created": len(chunks),
                "file_size_mb": file_size_mb,
                "point_ids": point_ids,
            }

        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            return None

    def ingest_directory(self, directory_path: Path) -> List[dict]:
        if not directory_path.exists() or not directory_path.is_dir():
            logger.error(f"Invalid directory: {directory_path}")
            return []

        supported_extensions = [".txt", ".pdf", ".docx", ".doc"]

        files = []
        for ext in supported_extensions:
            files.extend(directory_path.glob(f"*{ext}"))

        logger.info(f"Found {len(files)} documents to ingest")

        results = []
        for file_path in files:
            result = self.ingest_document(file_path)
            if result:
                results.append(result)

        logger.info(f"Successfully ingested {len(results)}/{len(files)} documents")
        return results

    def delete_document(self, document_id: str) -> bool:
        return self.vector_db.delete_by_document(document_id)


_ingestion_service_instance = None


def get_ingestion_service() -> IngestionService:
    global _ingestion_service_instance
    if _ingestion_service_instance is None:
        _ingestion_service_instance = IngestionService()
    return _ingestion_service_instance