from fastapi import APIRouter
from pydantic import BaseModel
from services.match_service import match_service_instance

router = APIRouter()

class MatchRequest(BaseModel):
    client_id: str
    niche_id: str

@router.post("/")
def make_match(request: MatchRequest):
    return match_service_instance.match(
        client_id=request.client_id,
        niche_id=request.niche_id
    )
