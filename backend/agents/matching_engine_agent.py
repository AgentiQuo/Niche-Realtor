from typing import Dict, Any, List, Tuple
import numpy as np

# We'll use the cosine_similarity from vector_utils
from embeddings.vector_utils import cosine_similarity
from models.tag import Tag

class MatchingEngineAgent:
    """
    Agent 5 — Matching Engine Agent
    Purpose: Match clients ↔ niches ↔ properties ↔ neighborhoods.
    Input: client embedding + niche embedding
    Output: ranked recommendations + explanations
    """
    
    def match(self, client_embedding: List[float], niche_embedding: List[float], candidate_properties: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Receives embeddings and a list of candidates, returns ranked results and explanations.
        """
        c_vec = np.array(client_embedding)
        n_vec = np.array(niche_embedding)
        
        # Combine client and niche preference for the final search vector
        # (This is a simplified approach, in reality you'd weight them)
        search_vec = c_vec + n_vec
        search_norm = np.linalg.norm(search_vec)
        if search_norm > 0:
            search_vec = search_vec / search_norm
        
        # Compute scores
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
            
        # Rank results
        scored_candidates.sort(key=lambda x: x["match_score"], reverse=True)
        ranked_results = scored_candidates[:10]
        
        # Generate explanations
        explanations = []
        for r in ranked_results:
            tags = r.get("tags", [])
            tag_names = [t["name"] if isinstance(t, dict) else t.name for t in tags[:3]]
            
            explanations.append({
                "property_id": r["property_id"],
                "text": "This property strongly aligns with your location and size preferences.",
                "aligned_tags": tag_names,
                "neighborhood_alignment": "Fits your desired vibe profile based on your current niche."
            })
            
        return ranked_results, explanations

matching_engine_agent = MatchingEngineAgent()
