from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from services.property_service import property_service_instance

router = APIRouter()

class PropertyIngestRequest(BaseModel):
    url: str
    images: List[str] = []
    metadata: Dict[str, Any] = {}

class PropertyAnalyzeRequest(BaseModel):
    property_id: str

@router.post("/ingest")
def ingest_property(request: PropertyIngestRequest):
    property_id = property_service_instance.ingest_property(
        url=request.url,
        images=request.images,
        metadata=request.metadata
    )
    return {"property_id": property_id}

@router.post("/analyze")
def analyze_property(request: PropertyAnalyzeRequest):
    return property_service_instance.analyze_property(request.property_id)
