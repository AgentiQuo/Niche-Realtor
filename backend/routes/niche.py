from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from models.niche import Niche
from models.tag import Tag
from services.niche_service import niche_service_instance

router = APIRouter()

class NicheCreateRequest(BaseModel):
    name: str
    description: str
    sources: List[str] = []
    tags: List[Tag] = []

@router.post("/create")
def create_niche(request: NicheCreateRequest):
    niche_id = niche_service_instance.create_niche(
        name=request.name,
        description=request.description,
        sources=request.sources,
        tags=request.tags
    )
    return {"niche_id": niche_id}

@router.get("/list", response_model=List[Niche])
def list_niches(page: int = 1, limit: int = 50):
    return niche_service_instance.list_niches(page=page, limit=limit)
