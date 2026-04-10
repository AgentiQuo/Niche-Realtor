from typing import Optional, List
from pydantic import BaseModel, conlist

class Tag(BaseModel):
    tag_id: str
    name: str
    polarity: str # positive, neutral, negative
    relevance: float
    confidence: float
    embedding: List[float]
    source: str # image, text, neighborhood
