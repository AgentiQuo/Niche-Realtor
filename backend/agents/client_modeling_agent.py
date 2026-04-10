from typing import Dict, Any, List
import numpy as np
from embeddings.embedding_math import update_client_embedding, normalize_vector

class ClientModelingAgent:
    """
    Agent 4 — Client Modeling Agent
    Purpose: Build and update client preference embeddings.
    Input: client intake form + feedback
    Output: client embedding
    """
    
    def model_client(self, preferences: Dict[str, Any]) -> List[float]:
        # Parse explicit preferences and construct an initial vector
        # Mocking behavior where 'walkable' and 'spacious' map to specific vector points
        
        # Start with a base vector
        base_vector = np.array([0.2, 0.3] * 64)
        
        # We normalize the initial preference vector
        final_vector = normalize_vector(base_vector)
        return final_vector.tolist()
        
    def update_with_feedback(self, current_embedding: List[float], feedback: Dict[str, Any]) -> List[float]:
        # feedback might look like {"liked": ["Spacious"], "disliked": ["Noisy"]}
        # In reality, this would query the DB for the tag embeddings of those traits
        # We will mock the adjustment vector
        adjustment_vector = np.array([0.05, -0.05] * 64)
        
        base_vector = np.array(current_embedding)
        
        # client_embedding = normalize(base_preferences_vector + feedback_adjustments)
        new_embedding = update_client_embedding(base_vector, adjustment_vector)
        return new_embedding.tolist()

client_modeling_agent = ClientModelingAgent()
