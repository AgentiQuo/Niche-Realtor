from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class Client(BaseModel):
    client_id: str
    preferences: Dict[str, Any] = {}
    embedding: List[float] = []
    feedback_history: List[Dict[str, Any]] = []
