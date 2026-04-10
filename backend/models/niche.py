from typing import Optional, List
from pydantic import BaseModel
from .tag import Tag
from .neighborhood import Neighborhood

class Niche(BaseModel):
    niche_id: str
    name: str
    description: str
    tags: List[Tag] = []
    neighborhoods: List[Neighborhood] = []
    embedding: List[float] = []
    sources: List[str] = []
