from typing import List, Dict, Any
from embeddings.vector_utils import cosine_similarity
import numpy as np

class VectorDB:
    def __init__(self):
        # In-memory storage: { collection_name: { item_id: { "vector": [], "metadata": {} } } }
        self.store: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def insert(self, collection_name: str, item_id: str, vector: List[float], metadata: Dict[str, Any] = None):
        if collection_name not in self.store:
            self.store[collection_name] = {}
        
        self.store[collection_name][item_id] = {
            "vector": vector,
            "metadata": metadata or {}
        }

    def search(self, collection_name: str, query_vector: List[float], top_k: int = 10) -> List[Dict[str, Any]]:
        if collection_name not in self.store:
            return []
            
        q_vec = np.array(query_vector)
        results = []
        
        for item_id, data in self.store[collection_name].items():
            stored_vec = np.array(data["vector"])
            score = cosine_similarity(q_vec, stored_vec)
            # Handle possible nan from zero vectors
            if np.isnan(score):
                score = 0.0
                
            results.append({
                "id": item_id,
                "score": float(score),
                "metadata": data["metadata"]
            })
            
        # Sort descending by score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

# Global singleton for in-memory DB
vector_db_instance = VectorDB()
