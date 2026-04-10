from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from services.client_service import client_service_instance

router = APIRouter()

class ClientCreateRequest(BaseModel):
    preferences: Dict[str, Any]

class ClientUpdateRequest(BaseModel):
    client_id: str
    feedback: Dict[str, Any]

@router.post("/create")
def create_client(request: ClientCreateRequest):
    client_id = client_service_instance.create_client(request.preferences)
    return {"client_id": client_id}

@router.post("/update")
def update_client(request: ClientUpdateRequest):
    updated_embedding = client_service_instance.update_client(
        client_id=request.client_id,
        feedback=request.feedback
    )
    return {"updated_client_embedding": updated_embedding}
