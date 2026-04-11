from pydantic import BaseModel
from typing import Dict, Any, List
from models.niche import Niche

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

class SimilarRequest(BaseModel):
    niche_id: str
    limit: int = 10

class MatchRequest(BaseModel):
    profile: Dict[str, Any]
    limit: int = 10

class NicheScored(Niche):
    similarity_score: float
