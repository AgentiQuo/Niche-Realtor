import uuid
from typing import List, Dict, Any
from db.relational_db import relational_db_instance
from db.vector_db import vector_db_instance
from embeddings.embedding_math import construct_tag_vector, compute_niche_embedding
from models.niche import Niche
from models.tag import Tag
import numpy as np

class NicheService:
    def create_niche(self, name: str, description: str, sources: List[str], tags: List[Tag]) -> str:
        niche_id = str(uuid.uuid4())
        
        # 1. Compute embedding (sum of tag vectors)
        tag_vectors = []
        for t in tags:
            vec = construct_tag_vector(t.relevance, t.embedding, t.polarity)
            tag_vectors.append(vec)
            
        # The spec also sums neighborhood_vectors, but at creation we might not have any yet.
        # We'll just sum the tag_vectors for now.
        neighborhood_vectors: List[np.ndarray] = []
        
        # Using the math from embeddings/embedding_math.py
        final_embedding = compute_niche_embedding(tag_vectors, neighborhood_vectors).tolist()
        
        # 2. Construct Niche model
        niche = Niche(
            niche_id=niche_id,
            name=name,
            description=description,
            tags=tags,
            neighborhoods=[], # Can be added later
            embedding=final_embedding,
            sources=sources
        )
        
        # 3. Store in DB
        relational_db_instance.insert_or_update("niches", niche_id, niche.model_dump())
        vector_db_instance.insert("niches", niche_id, final_embedding, metadata={"name": name})
        
        return niche_id

    def list_niches(self, page: int = 1, limit: int = 50) -> List[Dict[str, Any]]:
        # In a real impl, we'd use skip=(page-1)*limit, limit=limit
        niches = relational_db_instance.list_all("niches")
        return niches

niche_service_instance = NicheService()
