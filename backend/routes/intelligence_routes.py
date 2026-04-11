from fastapi import APIRouter
from typing import List
from models.intelligence import (
    SearchRequest,
    SimilarRequest,
    MatchRequest,
    NicheScored
)
from services.intelligence_service import intelligence_service_instance

router = APIRouter()

@router.post("/search", response_model=List[NicheScored])
def search_niches(request: SearchRequest):
    return intelligence_service_instance.search_niches(
        query=request.query, 
        limit=request.limit
    )

@router.post("/similar", response_model=List[NicheScored])
def similar_niches(request: SimilarRequest):
    return intelligence_service_instance.find_similar_niches(
        niche_id=request.niche_id, 
        limit=request.limit
    )

@router.post("/match", response_model=List[NicheScored])
def match_niches(request: MatchRequest):
    return intelligence_service_instance.match_profile_to_niches(
        profile=request.profile, 
        limit=request.limit
    )
