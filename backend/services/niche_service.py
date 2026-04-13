import uuid
from typing import List, Dict, Any, Optional
from db.relational_db import relational_db_instance
from db.vector_db import vector_db_instance
from embeddings.embedding_math import construct_tag_vector, compute_niche_embedding, EMBEDDING_SIZE
from models.niche import Niche
from models.tag import Tag, TagInternal
import numpy as np
from services.embedding_service import embedding_service_instance

class NicheService:
    def create_niche(self, name: str, description: str, sources: List[str], tags: List[Tag]) -> str:
        niche_id = str(uuid.uuid4())
        
        internal_tags = []
        tag_vectors = []
        for t in tags:
            tag_id = str(uuid.uuid4())
            # GET REAL EMBEDDING
            t_embedding = embedding_service_instance.get_embedding(t.name)
            
            internal_tag = TagInternal(
                tag_id=tag_id,
                niche_id=niche_id,
                name=t.name,
                polarity="positive",
                relevance=1.0,
                confidence=1.0,
                embedding=t_embedding,
                source="text"
            )
            internal_tags.append(internal_tag)
            
            vec = construct_tag_vector(internal_tag.relevance, internal_tag.embedding, internal_tag.polarity)
            tag_vectors.append(vec)
            
            # Persist tag
            relational_db_instance.insert_or_update("tags", tag_id, internal_tag.model_dump())
            
        final_embedding = compute_niche_embedding(tag_vectors, []).tolist()
        
        niche_dict = {
            "niche_id": niche_id,
            "name": name,
            "description": description,
            "tags": [it.model_dump() for it in internal_tags],
            "neighborhoods": [],
            "embedding": final_embedding,
            "sources": sources
        }
        
        relational_db_instance.insert_or_update("niches", niche_id, niche_dict)
        vector_db_instance.insert("niches", niche_id, final_embedding, metadata={"name": name, "description": description})
        
        return niche_id

    def update_niche(self, niche_id: str, name: str, description: str, tags: List[Tag]) -> None:
        niche_data = relational_db_instance.get_by_id("niches", niche_id)
        if not niche_data:
            raise ValueError(f"Niche {niche_id} not found")
        
        # 1. Re-compute tags and embeddings
        internal_tags = []
        tag_vectors = []
        for t in tags:
            tag_id = str(uuid.uuid4())
            t_embedding = embedding_service_instance.get_embedding(t.name)
            
            internal_tag = TagInternal(
                tag_id=tag_id,
                niche_id=niche_id,
                name=t.name,
                polarity="positive",
                relevance=1.0,
                confidence=1.0,
                embedding=t_embedding,
                source="text"
            )
            internal_tags.append(internal_tag)
            tag_vectors.append(construct_tag_vector(1.0, t_embedding, "positive"))
            relational_db_instance.insert_or_update("tags", tag_id, internal_tag.model_dump())
            
        # 2. Maintain existing neighborhoods if any
        neighborhood_vectors = []
        for n_dict in niche_data.get("neighborhoods", []):
            if "embedding" in n_dict and n_dict["embedding"]:
                neighborhood_vectors.append(np.array(n_dict["embedding"]))
        
        final_embedding = compute_niche_embedding(tag_vectors, neighborhood_vectors).tolist()
        
        # 3. Update storage
        niche_data["name"] = name
        niche_data["description"] = description
        niche_data["tags"] = [it.model_dump() for it in internal_tags]
        niche_data["embedding"] = final_embedding
        
        relational_db_instance.insert_or_update("niches", niche_id, niche_data)
        vector_db_instance.insert("niches", niche_id, final_embedding, metadata={"name": name, "description": description})

    def list_niches(self, page: int = 1, limit: int = 50) -> List[Dict[str, Any]]:
        return relational_db_instance.list_all("niches")

    def recompute_niche_embedding(self, niche_id: str) -> List[float]:
        niche_data = relational_db_instance.get_by_id("niches", niche_id)
        if not niche_data:
            return []
        
        tag_vectors = []
        updated_tags = []
        for t_dict in niche_data.get("tags", []):
            # Refresh embedding
            new_emb = embedding_service_instance.get_embedding(t_dict["name"])
            t_dict["embedding"] = new_emb
            updated_tags.append(t_dict)
            
            it = TagInternal(**t_dict)
            vec = construct_tag_vector(it.relevance, it.embedding, it.polarity)
            tag_vectors.append(vec)
            
        neighborhood_vectors = []
        for n_dict in niche_data.get("neighborhoods", []):
            if "embedding" in n_dict and n_dict["embedding"]:
                neighborhood_vectors.append(np.array(n_dict["embedding"]))
        
        if not tag_vectors and not neighborhood_vectors:
            # Fallback to name/desc
            text = niche_data["name"] + " " + niche_data["description"]
            final_embedding = np.array(embedding_service_instance.get_embedding(text))
        else:
            final_embedding = compute_niche_embedding(tag_vectors, neighborhood_vectors)
        
        niche_data["tags"] = updated_tags
        niche_data["embedding"] = final_embedding.tolist()
        
        relational_db_instance.insert_or_update("niches", niche_id, niche_data)
        vector_db_instance.insert("niches", niche_id, niche_data["embedding"], metadata={"name": niche_data["name"], "description": niche_data["description"]})
        
        return niche_data["embedding"]

    def recompute_all(self) -> Dict[str, int]:
        niches = relational_db_instance.list_all("niches")
        count = 0
        for niche in niches:
            self.recompute_niche_embedding(niche["niche_id"])
            count += 1
        return {"recomputed_count": count}

niche_service_instance = NicheService()
