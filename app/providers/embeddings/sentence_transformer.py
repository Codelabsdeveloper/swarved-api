
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

from app.providers.embeddings.base import BaseEmbeddingProvider
from app.core.constants.messages import ErrorMessages, SuccessMessages, InfoMessages
from app.core.exceptions import EmbeddingException
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SentenceTransformerProvider(BaseEmbeddingProvider):
    
    def __init__(
        self,
        model_name: str,
        dimension: int,
        device: str = "cpu"
    ):
        super().__init__(model_name, dimension)
        self.device = device
        self.model = None
        self._load_model()
    
    def _load_model(self) -> None:
        try:
            logger.info(InfoMessages.EMBEDDING_MODEL_LOADING.format(model=self.model_name))
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info(SuccessMessages.EMBEDDING_MODEL_LOADED.format(device=self.device))
        except Exception as e:
            error_msg = ErrorMessages.EMBEDDING_LOAD_FAILED.format(error=str(e))
            logger.error(error_msg)
            raise EmbeddingException(error_msg)
    
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        if not texts:
            logger.warning(ErrorMessages.EMBEDDING_EMPTY_INPUT)
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
            
            logger.debug(SuccessMessages.EMBEDDINGS_GENERATED.format(count=len(texts)))
            return embeddings
            
        except Exception as e:
            error_msg = ErrorMessages.EMBEDDING_GENERATION_FAILED.format(error=str(e))
            logger.error(error_msg)
            raise EmbeddingException(error_msg)