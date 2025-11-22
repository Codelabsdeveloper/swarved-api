from typing import List, Dict, Any
from app.config import settings
from app.utils.logger import get_logger
from app.models.embedding import get_embedding_model
from app.models.llm_model import get_llm_model
from app.services.vector_db import get_vector_db
from app.models.schemas import QueryRequest, QueryResponse, Source

logger = get_logger(__name__)


class RAGPipeline:

    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.llm_model = get_llm_model()
        self.vector_db = get_vector_db()

    def process_query(self, request: QueryRequest) -> QueryResponse:
        try:
            logger.info(f"Processing query: {request.message[:100]}...")

            query_embedding = self.embedding_model.embed_query(request.message)

            top_k = request.top_k or settings.TOP_K_RETRIEVAL
            search_results = self.vector_db.search(
                query_vector=query_embedding.tolist(),
                top_k=top_k,
                score_threshold=settings.SIMILARITY_THRESHOLD,
            )

            logger.info(f"Retrieved {len(search_results)} relevant chunks")

            if not search_results:
                return QueryResponse(
                    answer="The provided documents do not contain this information.",
                    sources=[],
                    language=request.language or "en",
                    confidence=0.0,
                )

            context_texts = []
            sources = []

            for result in search_results:
                payload = result["payload"]
                context_texts.append(payload["text"])

                sources.append(
                    Source(
                        document_name=payload.get("document_name", "Unknown"),
                        content=payload["text"][:200] + "...",
                        score=round(result["score"], 3),
                        page=payload.get("page"),
                    )
                )

            history = [
                {"role": msg.role, "content": msg.content} for msg in request.history
            ]

            answer = self.llm_model.generate(
                prompt=request.message,
                context=context_texts,
                history=history if history else None,
            )

            avg_confidence = sum(r["score"] for r in search_results) / len(
                search_results
            )

            logger.info("Successfully generated answer")

            return QueryResponse(
                answer=answer,
                sources=sources,
                language=request.language or "en",
                confidence=round(avg_confidence, 3),
            )

        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}")
            return QueryResponse(
                answer=f"An error occurred while processing your query: {str(e)}",
                sources=[],
                language=request.language or "en",
                confidence=0.0,
            )

    def retrieve_only(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        try:
            query_embedding = self.embedding_model.embed_query(query)
            results = self.vector_db.search(
                query_vector=query_embedding.tolist(), top_k=top_k
            )
            return results
        except Exception as e:
            logger.error(f"Error in retrieval: {e}")
            return []


_rag_pipeline_instance = None


def get_rag_pipeline() -> RAGPipeline:
    global _rag_pipeline_instance
    if _rag_pipeline_instance is None:
        _rag_pipeline_instance = RAGPipeline()
    return _rag_pipeline_instance
