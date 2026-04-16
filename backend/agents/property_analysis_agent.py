from typing import Dict, Any, Tuple, List
import uuid
import json
import numpy as np

from embeddings.embedding_math import construct_tag_vector, compute_property_embedding
from models.tag import Tag
from services.llm_service import llm_service_instance
from utils.agent_config import get_agent_config

class PropertyAnalysisAgent:
    """
    Agent 2 — Property Analysis Agent
    Purpose: Convert property images + text into qualitative tags and embeddings.
    """
    def __init__(self):
        self.config = get_agent_config("property_analysis")

    def analyze(self, property_data: Dict[str, Any]) -> Tuple[List[Tag], List[float]]:
        """
        Uses an LLM to generate qualitative tags, then computes a weighted embedding.
        """
        metadata = property_data.get("metadata", {})
        
        system_prompt = """
        You are an Architectural and Lifestyle Analyst.
        Generate qualitative tags for a property based on its description and metadata.
        For each tag, provide:
        1. name (the quality, e.g., "Natural Light", "Modern", "Spacious")
        2. polarity ("positive" or "negative")
        3. relevance (1.0 to 10.0)
        4. confidence (0.0 to 1.0)
        Return ONLY a JSON list of objects.
        """
        
        prompt = f"Analyze this property: {json.dumps(metadata)}"
        
        response = llm_service_instance.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            model=self.config.get("model"),
            temperature=self.config.get("temperature", 0.2)
        )
        
        try:
            raw_tags = json.loads(response)
            tags = []
            for rt in raw_tags:
                # In a real system, you'd call an embedding service for each tag name here
                # Mocking tag embedding for this demonstration
                mock_tag_embedding = [0.1 * len(rt.get("name", ""))] * 128
                
                tags.append(Tag(
                    tag_id=str(uuid.uuid4()),
                    name=rt.get("name", "Unknown"),
                    polarity=rt.get("polarity", "positive"),
                    relevance=float(rt.get("relevance", 5.0)),
                    confidence=float(rt.get("confidence", 0.5)),
                    embedding=mock_tag_embedding,
                    source="llm_analysis"
                ))
        except Exception as e:
            print(f"Error parsing analysis tags: {e}. Using fallback.")
            tags = [Tag(
                tag_id=str(uuid.uuid4()),
                name="Spacious",
                polarity="positive",
                relevance=8.0,
                confidence=0.9,
                embedding=[0.1] * 128,
                source="fallback"
            )]
        
        # Extract and sum vectors according to BC-4 spec
        tag_vectors = []
        for t in tags:
            vec = construct_tag_vector(t.relevance, t.embedding, t.polarity)
            tag_vectors.append(vec)
            
        final_embedding = compute_property_embedding(tag_vectors).tolist()
        
        return tags, final_embedding

property_analysis_agent = PropertyAnalysisAgent()
