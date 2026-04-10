from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from .tag import Tag

class Property(BaseModel):
    property_id: str
    images: List[str] = []
    tags: List[Tag] = []
    embedding: List[float] = []
    location: str
    metadata: Dict[str, Any] = {}
