from typing import List, Dict, Any, Optional
import uuid
import pickle
from pathlib import Path
import numpy as np
import faiss
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class VectorDatabase:
    
    def __init__(self):
        self.dimension = settings.EMBEDDING_DIMENSION
        self.index_file = settings.VECTOR_STORE_DIR / "faiss_index.bin"
        self.metadata_file = settings.VECTOR_STORE_DIR / "faiss_metadata.pkl"
        
        self.index = None
        self.metadata = []  # Store metadata for each vector
        
        self._load_or_create_index()
    
    def _load_or_create_index(self) -> None:
        try:
            if self.index_file.exists() and self.metadata_file.exists():
                logger.info(f"Loading existing FAISS index from: {self.index_file}")
                self.index = faiss.read_index(str(self.index_file))
                
                with open(self.metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)
                
                logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
            else:
                logger.info("Creating new FAISS index")
                self.index = faiss.IndexFlatIP(self.dimension)
                self.metadata = []
                logger.info("New FAISS index created")
                
        except Exception as e:
            logger.error(f"Error loading/creating FAISS index: {e}")
            self.index = faiss.IndexFlatIP(self.dimension)
            self.metadata = []
    
    def _save_index(self) -> None:
        try:
            faiss.write_index(self.index, str(self.index_file))
            
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)
            
            logger.debug("FAISS index saved to disk")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {e}")
    
    def add_vectors(
        self,
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]]
    ) -> List[str]:
        if len(vectors) != len(payloads):
            raise ValueError("Number of vectors and payloads must match")
        
        try:
            vectors_np = np.array(vectors, dtype=np.float32)
            faiss.normalize_L2(vectors_np)
            
            ids = [str(uuid.uuid4()) for _ in range(len(vectors))]
            
            for payload, vec_id in zip(payloads, ids):
                payload['id'] = vec_id
            
            self.index.add(vectors_np)
            self.metadata.extend(payloads)
            
            self._save_index()
            logger.info(f"Added {len(ids)} vectors to FAISS index")
            return ids
            
        except Exception as e:
            logger.error(f"Error adding vectors to FAISS: {e}")
            raise
    
    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        score_threshold: Optional[float] = None,
        filter_conditions: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        try:
            if self.index.ntotal == 0:
                logger.warning("FAISS index is empty")
                return []
            
            query_np = np.array([query_vector], dtype=np.float32)
            faiss.normalize_L2(query_np)
            
            search_k = top_k * 3 if filter_conditions else top_k
            search_k = min(search_k, self.index.ntotal)
            
            distances, indices = self.index.search(query_np, search_k)
            
            formatted_results = []
            
            for dist, idx in zip(distances[0], indices[0]):
                if idx == -1:
                    continue
                
                similarity = float(dist)
                
                if score_threshold and similarity < score_threshold:
                    continue
                
                metadata = self.metadata[idx].copy()
                
                if filter_conditions:
                    match = all(
                        metadata.get(key) == value 
                        for key, value in filter_conditions.items()
                    )
                    if not match:
                        continue
                
                result = {
                    "id": metadata.get('id', str(idx)),
                    "score": similarity,
                    "payload": metadata
                }
                formatted_results.append(result)
                
                if len(formatted_results) >= top_k:
                    break
            
            logger.info(f"Found {len(formatted_results)} similar vectors in FAISS")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching vectors in FAISS: {e}")
            return []
    
    def delete_by_document(self, document_id: str) -> bool:
        try:
            new_metadata = [
                m for m in self.metadata 
                if m.get('document_id') != document_id
            ]
            
            if len(new_metadata) == len(self.metadata):
                logger.warning(f"No vectors found for document: {document_id}")
                return False
            
            logger.info(f"Rebuilding FAISS index after deleting document: {document_id}")
            new_index = faiss.IndexFlatIP(self.dimension)
            
            if new_metadata:
                logger.warning("FAISS deletion requires rebuilding. Consider re-ingesting documents.")
            
            self.index = new_index
            self.metadata = new_metadata
            self._save_index()
            
            logger.info(f"Deleted vectors for document: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting vectors from FAISS: {e}")
            return False
    
    def count_documents(self) -> int:
        try:
            return self.index.ntotal
        except Exception as e:
            logger.error(f"Error counting documents in FAISS: {e}")
            return 0
    
    def health_check(self) -> bool:
        try:
            return self.index is not None
        except Exception as e:
            logger.error(f"FAISS health check failed: {e}")
            return False
    
    def reset_index(self) -> bool:
        try:
            self.index = faiss.IndexFlatIP(self.dimension)
            self.metadata = []
            self._save_index()
            logger.warning("FAISS index has been reset")
            return True
        except Exception as e:
            logger.error(f"Error resetting FAISS index: {e}")
            return False


# Global vector database instance
_vector_db_instance = None


def get_vector_db() -> VectorDatabase:
    global _vector_db_instance
    if _vector_db_instance is None:
        _vector_db_instance = VectorDatabase()
    return _vector_db_instance