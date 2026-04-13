import httpx
from typing import List
from config.settings import settings
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.url = "https://api.openai.com/v1/embeddings"

    def get_embedding(self, text: str) -> List[float]:
        if not self.api_key:
            # Fallback for local development if no key is provided
            # Standardizing a deterministic fallback instead of random
            print("Warning: No OPENAI_API_KEY found. Using deterministic mock embedding.")
            return self._mock_embedding(text)

        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            payload = {
                "input": text,
                "model": "text-embedding-3-small"
            }
            response = httpx.post(self.url, headers=headers, json=payload, timeout=10.0)
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            print(f"Error calling OpenAI embeddings: {e}. Falling back to mock.")
            return self._mock_embedding(text)

    def _mock_embedding(self, text: str) -> List[float]:
        # Deterministic non-zero vector based on hash
        size = 1536
        seed = sum(ord(c) for c in text) % 10000
        rng = np.random.default_rng(seed)
        vec = rng.standard_normal(size)
        # Normalize
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

embedding_service_instance = EmbeddingService()
