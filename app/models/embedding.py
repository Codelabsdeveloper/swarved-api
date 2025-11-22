from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingModel:

    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL_NAME
        self.device = settings.EMBEDDING_DEVICE
        self.dimension = settings.EMBEDDING_DIMENSION
        self.model = None
        self._load_model()

    def _load_model(self) -> None:
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info(f"Embedding model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        if not texts:
            logger.warning("Empty input to embed()")
            return np.array([])

        if isinstance(texts, str):
            texts = [texts]

        try:
            embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False,
                normalize_embeddings=True,
            )

            logger.debug(f"Generated embeddings for {len(texts)} texts")
            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def embed_query(self, query: str) -> np.ndarray:
        embedding = self.embed([query])
        return embedding[0] if len(embedding) > 0 else np.array([])

    def embed_documents(self, documents: List[str]) -> np.ndarray:
        return self.embed(documents)

    def get_dimension(self) -> int:
        return self.dimension


_embedding_model_instance = None


def get_embedding_model() -> EmbeddingModel:
    global _embedding_model_instance
    if _embedding_model_instance is None:
        _embedding_model_instance = EmbeddingModel()
    return _embedding_model_instance