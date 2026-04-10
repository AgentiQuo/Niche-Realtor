import uuid
from typing import Dict, Any, List
from db.relational_db import relational_db_instance
from db.vector_db import vector_db_instance
from models.client import Client

# Import Agent
from agents.client_modeling_agent import client_modeling_agent

class ClientService:
    def create_client(self, preferences: Dict[str, Any]) -> str:
        client_id = str(uuid.uuid4())
        
        # Agent 4 generates modeled vector
        modeled_embedding = client_modeling_agent.model_client(preferences)
        
        client = Client(
            client_id=client_id,
            preferences=preferences,
            embedding=modeled_embedding,
            feedback_history=[]
        )
        
        relational_db_instance.insert_or_update("clients", client_id, client.model_dump())
        vector_db_instance.insert("clients", client_id, modeled_embedding, metadata={"id": client_id})
        
        return client_id

    def update_client(self, client_id: str, feedback: Dict[str, Any]) -> List[float]:
        client_data = relational_db_instance.get_by_id("clients", client_id)
        if not client_data:
            raise ValueError(f"Client {client_id} not found")
            
        client_data["feedback_history"].append(feedback)
        
        # Agent 4 runs feedback loop through Embedding Engine
        updated_embedding = client_modeling_agent.update_with_feedback(client_data["embedding"], feedback)
        client_data["embedding"] = updated_embedding
        
        relational_db_instance.insert_or_update("clients", client_id, client_data)
        vector_db_instance.insert("clients", client_id, updated_embedding, metadata={"id": client_id})
        
        return updated_embedding

client_service_instance = ClientService()
