import uuid
from typing import List, Dict, Any
from db.relational_db import relational_db_instance
from db.vector_db import vector_db_instance
from models.property import Property
from models.tag import Tag

# Import Agents!
from agents.listing_scraper import listing_scraper_agent
from agents.property_analysis_agent import property_analysis_agent

class PropertyService:
    def ingest_property(self, url: str, images: List[str], metadata: Dict[str, Any]) -> str:
        # Agent 1 handles logic mapping
        listing_obj = listing_scraper_agent.extract(url)
        
        # Merge fetched metadata
        merged_metadata = {**listing_obj.get("metadata", {}), **metadata}
        
        property_id = str(uuid.uuid4())
        prop = Property(
            property_id=property_id,
            images=images or listing_obj.get("images", []),
            tags=[], 
            embedding=[], 
            location=merged_metadata.get("location", "Unknown"),
            metadata=merged_metadata
        )
        
        relational_db_instance.insert_or_update("properties", property_id, prop.model_dump())
        return property_id

    def analyze_property(self, property_id: str) -> Dict[str, Any]:
        prop_data = relational_db_instance.get_by_id("properties", property_id)
        if not prop_data:
            raise ValueError(f"Property {property_id} not found")
            
        # Agent 2 handles vision, tags, and embedding generation
        tags, final_embedding = property_analysis_agent.analyze(prop_data)
        
        prop_data["tags"] = [t.model_dump() for t in tags]
        prop_data["embedding"] = final_embedding
        
        relational_db_instance.insert_or_update("properties", property_id, prop_data)
        vector_db_instance.insert("properties", property_id, final_embedding, metadata={"location": prop_data.get("location")})
        
        return {
            "tags": prop_data["tags"],
            "embedding": final_embedding
        }

property_service_instance = PropertyService()
