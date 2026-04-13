from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from models.niche import Niche
from models.tag import Tag
from services.niche_service import niche_service_instance
from models.niche_responses import NicheCreateResponse

router = APIRouter()

class NicheCreateRequest(BaseModel):
    name: str
    description: str
    sources: List[str] = []
    tags: List[Tag] = []

class NicheUpdateRequest(BaseModel):
    name: str
    description: str
    tags: List[Tag] = []

@router.post("/create", response_model=NicheCreateResponse)
def create_niche(request: NicheCreateRequest):
    niche_id = niche_service_instance.create_niche(
        name=request.name,
        description=request.description,
        sources=request.sources,
        tags=request.tags
    )
    return NicheCreateResponse(niche_id=niche_id)

@router.put("/{niche_id}", response_model=dict)
def update_niche(niche_id: str, request: NicheUpdateRequest):
    niche_service_instance.update_niche(
        niche_id=niche_id,
        name=request.name,
        description=request.description,
        tags=request.tags
    )
    return {"status": "success", "niche_id": niche_id}

@router.get("/list", response_model=List[Niche])
def list_niches(page: int = 1, limit: int = 50):
    return niche_service_instance.list_niches(page=page, limit=limit)

