from typing import List, Dict, Any
from db.vector_db import vector_db_instance
from db.relational_db import relational_db_instance
from services.embedding_service import embedding_service_instance
import json


class IntelligenceService:
    def _text_to_embedding(self, text: str) -> List[float]:
        return embedding_service_instance.get_embedding(text)
    
    def _profile_to_embedding(self, profile: Dict[str, Any]) -> List[float]:
        text_rep = json.dumps(profile, sort_keys=True)
        return embedding_service_instance.get_embedding(text_rep)


    def search_niches(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        query_vector = self._text_to_embedding(query)
        victors = vector_db_instance.search("niches", query_vector, top_k=limit)
        return self._build_scored_results(victors)
        
    def find_similar_niches(self, niche_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        niche = relational_db_instance.get_by_id("niches", niche_id)
        if not niche or not niche.get("embedding"):
            return []
            
        victors = vector_db_instance.search("niches", niche["embedding"], top_k=limit + 1)
        victors = [v for v in victors if v["id"] != niche_id][:limit]
        return self._build_scored_results(victors)

    def match_profile_to_niches(self, profile: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        profile_vector = self._profile_to_embedding(profile)
        victors = vector_db_instance.search("niches", profile_vector, top_k=limit)

        return self._build_scored_results(victors)

    def _build_scored_results(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        scored_niches = []
        for result in search_results:
            niche_id = result["id"]
            score = result["score"]
            niche_data = relational_db_instance.get_by_id("niches", niche_id)
            if niche_data:
                niche_copy = dict(niche_data)
                niche_copy["similarity_score"] = score
                scored_niches.append(niche_copy)
        return scored_niches

intelligence_service_instance = IntelligenceService()
