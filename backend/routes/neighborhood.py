from fastapi import APIRouter
from pydantic import BaseModel
from services.neighborhood_service import neighborhood_service_instance

router = APIRouter()

class NeighborhoodAnalyzeRequest(BaseModel):
    neighborhood_name: str
    region: str

@router.post("/analyze")
def analyze_neighborhood(request: NeighborhoodAnalyzeRequest):
    return neighborhood_service_instance.analyze_neighborhood(
        neighborhood_name=request.neighborhood_name,
        region=request.region
    )
