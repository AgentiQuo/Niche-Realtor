import uuid
from typing import Dict, Any
from db.relational_db import relational_db_instance
from db.vector_db import vector_db_instance
from models.neighborhood import Neighborhood

# Import Agent
from agents.neighborhood_scout_agent import neighborhood_scout_agent

class NeighborhoodService:
    def analyze_neighborhood(self, neighborhood_name: str, region: str) -> Dict[str, Any]:
        neighborhood_id = str(uuid.uuid4())
        
        # Agent 3 handles scouting
        tags, final_embedding, vibe_summary = neighborhood_scout_agent.scout(neighborhood_name, region)
        
        neighbor = Neighborhood(
            neighborhood_id=neighborhood_id,
            name=neighborhood_name,
            region=region,
            tags=tags,
            embedding=final_embedding,
            similar_neighborhoods=[],
            vibe_summary=vibe_summary,
            match_score=0.0
        )
        
        relational_db_instance.insert_or_update("neighborhoods", neighborhood_id, neighbor.model_dump())
        vector_db_instance.insert("neighborhoods", neighborhood_id, final_embedding, metadata={"name": neighborhood_name})
        
        return {
            "tags": [t.model_dump() for t in tags],
            "embedding": final_embedding,
            "vibe_summary": vibe_summary
        }

neighborhood_service_instance = NeighborhoodService()
