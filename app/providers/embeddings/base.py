from abc import ABC, abstractmethod
from typing import List, Union
import numpy as np


class BaseEmbeddingProvider(ABC):
    
    def __init__(self, model_name: str, dimension: int):
        self.model_name = model_name
        self.dimension = dimension
    
    @abstractmethod
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        pass
    
    def embed_query(self, query: str) -> np.ndarray:
        embedding = self.embed([query])
        return embedding[0] if len(embedding) > 0 else np.array([])
    
    def embed_documents(self, documents: List[str]) -> np.ndarray:
        return self.embed(documents)
    
    def get_dimension(self) -> int:
        return self.dimension