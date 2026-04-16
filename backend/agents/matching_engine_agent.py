from typing import Dict, Any, List, Tuple
import numpy as np
import json

from embeddings.vector_utils import cosine_similarity
from models.tag import Tag
from services.llm_service import llm_service_instance
from utils.agent_config import get_agent_config

class MatchingEngineAgent:
    """
    Agent 5 — Matching Engine Agent
    Purpose: Match clients ↔ niches ↔ properties ↔ neighborhoods.
    """
    def __init__(self):
        self.config = get_agent_config("matching_engine")

    def match(self, client_embedding: List[float], niche_embedding: List[float], candidate_properties: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Receives embeddings and a list of candidates, returns ranked results and LLM-generated explanations.
        """
        c_vec = np.array(client_embedding)
        n_vec = np.array(niche_embedding)
        
        search_vec = c_vec + n_vec
        search_norm = np.linalg.norm(search_vec)
        if search_norm > 0:
            search_vec = search_vec / search_norm
        
        scored_candidates = []
        for prop in candidate_properties:
            p_vec = np.array(prop.get("embedding", []))
            if len(p_vec) == 0:
                continue
                
            score = cosine_similarity(search_vec, p_vec)
            if np.isnan(score):
                score = 0.0
            
            prop_copy = dict(prop)
            prop_copy["match_score"] = float(score)
            scored_candidates.append(prop_copy)
            
        scored_candidates.sort(key=lambda x: x["match_score"], reverse=True)
        ranked_results = scored_candidates[:5] # Reducing to 5 for speed and cost
        
        # Generate explanations using an LLM
        explanations = []
        for r in ranked_results:
            tags = r.get("tags", [])
            tag_names = [t["name"] if isinstance(t, dict) else t.name for t in tags[:3]]
            
            system_prompt = "You are a Real Estate Matchmaker. Explain why a property is a good match for a client based on tags and score."
            prompt = f"Property Tags: {tag_names}, Match Score: {r['match_score']:.2f}. Explain why this is a good fit."
            
            explanation_text = llm_service_instance.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                model=self.config.get("model"),
                temperature=self.config.get("temperature", 0.1),
                max_tokens=100
            )
            
            explanations.append({
                "property_id": r.get("property_id") or r.get("id"),
                "text": explanation_text,
                "aligned_tags": tag_names,
                "neighborhood_alignment": "This property matches your lifestyle profile."
            })
            
        return ranked_results, explanations

matching_engine_agent = MatchingEngineAgent()
