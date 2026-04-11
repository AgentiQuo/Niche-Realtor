from typing import Optional, List
from pydantic import BaseModel

class Tag(BaseModel):
    name: str

class TagInternal(Tag):
    tag_id: str
    niche_id: Optional[str] = None
    polarity: str = "positive"
    relevance: float = 1.0
    confidence: float = 1.0
    embedding: List[float] = []
    source: str = "text"
