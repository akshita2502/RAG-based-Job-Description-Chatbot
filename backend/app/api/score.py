from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ats_score import calculate_ats_score

router = APIRouter()

class ScoreRequest(BaseModel):
    job_id: str
    job_description: str

@router.post("/")
def get_ats_score(request: ScoreRequest):
    return calculate_ats_score(request.job_id, request.job_description)
