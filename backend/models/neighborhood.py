from typing import Optional, List
from pydantic import BaseModel
from .tag import Tag

class Neighborhood(BaseModel):
    neighborhood_id: str
    name: str
    region: str
    tags: List[Tag] = []
    embedding: List[float] = []
    similar_neighborhoods: List[str] = []
    vibe_summary: Optional[str] = None
    match_score: Optional[float] = None
