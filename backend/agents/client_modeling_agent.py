from typing import Dict, Any, List
import numpy as np
import json
from embeddings.embedding_math import update_client_embedding, normalize_vector, construct_tag_vector
from services.llm_service import llm_service_instance
from utils.agent_config import get_agent_config

class ClientModelingAgent:
    """
    Agent 4 — Client Modeling Agent
    Purpose: Build and update client preference embeddings.
    """
    def __init__(self):
        self.config = get_agent_config("client_modeling")

    def model_client(self, preferences: Dict[str, Any]) -> List[float]:
        """
        Uses an LLM to interpret natural language preferences into a starting embedding.
        """
        system_prompt = """
        You are a Real Estate Profiler. 
        Interpret the client's preferences and identify key qualitative traits they value.
        For each trait, provide a relevance score (1-10).
        Return ONLY valid JSON.
        """
        
        prompt = f"Summarize the starting preferences for this client: {json.dumps(preferences)}"
        
        response = llm_service_instance.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            model=self.config.get("model"),
            temperature=self.config.get("temperature", 0.2)
        )
        
        try:
            # Map LLM interpreted traits to a combined vector
            traits = json.loads(response)
            # Simplification: we sum up "mock" embeddings for each interpreted trait
            combined_vec = np.zeros(128)
            for trait, score in traits.items():
                if isinstance(score, (int, float)):
                    # Mocking a trait vector
                    trait_vec = [0.05 * len(trait)] * 128
                    vec = construct_tag_vector(float(score), trait_vec, "positive")
                    combined_vec += vec
            
            return normalize_vector(combined_vec).tolist()
        except:
            # Fallback
            return normalize_vector(np.array([0.2, 0.3] * 64)).tolist()
        
    def update_with_feedback(self, current_embedding: List[float], feedback: Dict[str, Any]) -> List[float]:
        """
        Adjusts the client profile based on feedback using an LLM to determine the shift direction.
        """
        system_prompt = "Analyze the user feedback and determine how it shifts their real estate preferences."
        prompt = f"Current Profile (context): {current_embedding[:5]}... Feedback: {json.dumps(feedback)}"
        
        # Here we could use the LLM to decide which dimensions to boost/dampen
        # For now, we'll use a mocked adjustment triggered by the LLM call
        response = llm_service_instance.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            model=self.config.get("model")
        )
        
        # Mocking adjustment based on having called the LLM
        adjustment_vector = np.array([0.05 if "like" in response.lower() else -0.05] * 128)
        
        base_vector = np.array(current_embedding)
        new_embedding = update_client_embedding(base_vector, adjustment_vector)
        return new_embedding.tolist()

client_modeling_agent = ClientModelingAgent()
