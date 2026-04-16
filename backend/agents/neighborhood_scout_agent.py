from typing import Dict, Any, Tuple, List
import uuid
import numpy as np
import json

from embeddings.embedding_math import construct_tag_vector, compute_neighborhood_embedding
from models.tag import Tag
from services.llm_service import llm_service_instance
from utils.agent_config import get_agent_config

class NeighborhoodScoutAgent:
    """
    Agent 3 — Neighborhood Scout Agent
    Purpose: Build qualitative profiles of neighborhoods.
    """
    def __init__(self):
        self.config = get_agent_config("neighborhood_scout")

    def scout(self, neighborhood_name: str, region: str) -> Tuple[List[Tag], List[float], str]:
        """
        Uses an LLM to scout and summarize the vibe of a neighborhood.
        """
        system_prompt = """
        You are a Local Neighborhood Scout.
        Analyze the specified neighborhood and provide:
        1. A set of qualitative tags with polarity, relevance, and confidence.
        2. A concise "vibe summary" (max 2 sentences).
        Return ONLY valid JSON.
        """
        
        prompt = f"Scout the neighborhood '{neighborhood_name}' in '{region}'."
        
        response = llm_service_instance.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            model=self.config.get("model"),
            temperature=self.config.get("temperature", 0.3)
        )
        
        try:
            data = json.loads(response)
            raw_tags = data.get("tags", [])
            vibe_summary = data.get("vibe_summary", f"A summary of {neighborhood_name}")
            
            tags = []
            for rt in raw_tags:
                mock_embed = [0.1 * len(rt.get("name", ""))] * 128
                tags.append(Tag(
                    tag_id=str(uuid.uuid4()),
                    name=rt.get("name", "Unknown"),
                    polarity=rt.get("polarity", "positive"),
                    relevance=float(rt.get("relevance", 5.0)),
                    confidence=float(rt.get("confidence", 0.5)),
                    embedding=mock_embed,
                    source="neighborhood_scout"
                ))
        except Exception:
            # Fallback
            tags = [Tag(
                tag_id=str(uuid.uuid4()),
                name="Vibrant",
                polarity="positive",
                relevance=8.0,
                confidence=0.8,
                embedding=[0.1] * 128,
                source="fallback"
            )]
            vibe_summary = f"{neighborhood_name} has a vibrant atmosphere."

        # Extract and sum vectors according to BC-4 spec
        tag_vectors = []
        for t in tags:
            vec = construct_tag_vector(t.relevance, t.embedding, t.polarity)
            tag_vectors.append(vec)
            
        final_embedding = compute_neighborhood_embedding(tag_vectors).tolist()
        
        return tags, final_embedding, vibe_summary

neighborhood_scout_agent = NeighborhoodScoutAgent()
