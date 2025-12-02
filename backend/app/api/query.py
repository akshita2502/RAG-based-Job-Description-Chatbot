# backend/app/api/query.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat import chat_with_jd

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    job_id: str  # <--- We now require the ID of the document we are talking about

@router.post("/")
def ask_question(request: QueryRequest):
    answer = chat_with_jd(request.query, request.job_id)
    return {"answer": answer}