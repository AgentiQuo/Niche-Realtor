import uuid
from typing import List, Dict, Any
from db.relational_db import relational_db_instance
from db.vector_db import vector_db_instance
from embeddings.embedding_math import construct_tag_vector, compute_niche_embedding, EMBEDDING_SIZE
from models.niche import Niche
from models.tag import Tag, TagInternal
import numpy as np

class NicheService:
    def create_niche(self, name: str, description: str, sources: List[str], tags: List[Tag]) -> str:
        niche_id = str(uuid.uuid4())
        
        # 1. Compute embedding and build internal tags
        internal_tags = []
        tag_vectors = []
        for t in tags:
            tag_id = str(uuid.uuid4())
            internal_tag = TagInternal(
                tag_id=tag_id,
                niche_id=niche_id,
                name=t.name,
                polarity="positive",
                relevance=1.0,
                confidence=1.0,
                embedding=[0.0] * EMBEDDING_SIZE,
                source="text"
            )
            internal_tags.append(internal_tag)
            
            vec = construct_tag_vector(internal_tag.relevance, internal_tag.embedding, internal_tag.polarity)
            tag_vectors.append(vec)
            
            # Persist tag independently in 'tags' collection
            relational_db_instance.insert_or_update("tags", tag_id, internal_tag.model_dump())
            
        # The spec also sums neighborhood_vectors, but at creation we might not have any yet.
        # We'll just sum the tag_vectors for now.
        neighborhood_vectors: List[np.ndarray] = []
        
        # Using the math from embeddings/embedding_math.py
        final_embedding = compute_niche_embedding(tag_vectors, neighborhood_vectors).tolist()
        
        # 2. Construct Niche storage dict
        niche_dict = {
            "niche_id": niche_id,
            "name": name,
            "description": description,
            "tags": [it.model_dump() for it in internal_tags],
            "neighborhoods": [],
            "embedding": final_embedding,
            "sources": sources
        }
        
        # 3. Store in DB
        relational_db_instance.insert_or_update("niches", niche_id, niche_dict)
        vector_db_instance.insert("niches", niche_id, final_embedding, metadata={"name": name})
        
        return niche_id

    def list_niches(self, page: int = 1, limit: int = 50) -> List[Dict[str, Any]]:
        # In a real impl, we'd use skip=(page-1)*limit, limit=limit
        niches = relational_db_instance.list_all("niches")
        return niches

niche_service_instance = NicheService()
