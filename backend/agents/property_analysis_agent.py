from typing import Dict, Any, Tuple
import uuid
import numpy as np

from embeddings.embedding_math import construct_tag_vector, compute_property_embedding
from models.tag import Tag

class PropertyAnalysisAgent:
    """
    Agent 2 — Property Analysis Agent
    Purpose: Convert property images + text into qualitative tags and embeddings.
    Input: ListingObject
    Output: property tags + property embedding
    """
    def analyze(self, property_data: Dict[str, Any]) -> Tuple[list[Tag], list[float]]:
        # Mocking vision and text extraction from an LLM
        # For a localized downtown property, we'll assign relevant tags
        
        # Base static embedding for "Spacious"
        embed1 = [0.1, 0.2] * 64 
        # Base static embedding for "Natural Light"
        embed2 = [0.2, 0.4] * 64
        
        tag1 = Tag(
            tag_id=str(uuid.uuid4()),
            name="Spacious",
            polarity="positive",
            relevance=8.5,
            confidence=0.9,
            embedding=embed1,
            source="text"
        )
        
        tag2 = Tag(
            tag_id=str(uuid.uuid4()),
            name="Natural Light",
            polarity="positive",
            relevance=9.0,
            confidence=0.95,
            embedding=embed2,
            source="image"
        )
        
        tags = [tag1, tag2]
        
        # Extract and sum vectors according to BC-4 spec
        tag_vectors = []
        for t in tags:
            vec = construct_tag_vector(t.relevance, t.embedding, t.polarity)
            tag_vectors.append(vec)
            
        final_embedding = compute_property_embedding(tag_vectors).tolist()
        
        return tags, final_embedding

property_analysis_agent = PropertyAnalysisAgent()
