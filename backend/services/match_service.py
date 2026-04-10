from typing import Dict, Any, List
from db.relational_db import relational_db_instance

# Import Agent
from agents.matching_engine_agent import matching_engine_agent

class MatchService:
    def match(self, client_id: str, niche_id: str) -> Dict[str, Any]:
        client_data = relational_db_instance.get_by_id("clients", client_id)
        niche_data = relational_db_instance.get_by_id("niches", niche_id)
        
        if not client_data or not niche_data:
            return {"ranked_results": [], "explanations": []}
            
        c_vec = client_data.get("embedding", [])
        n_vec = niche_data.get("embedding", [])
        
        # Load candidate properties
        candidate_props = relational_db_instance.list_all("properties")
        
        # Agent 5 handles computations, scoring, and explanations natively
        ranked_results, explanations = matching_engine_agent.match(c_vec, n_vec, candidate_props)
        
        return {
            "ranked_results": ranked_results,
            "explanations": explanations
        }

match_service_instance = MatchService()
