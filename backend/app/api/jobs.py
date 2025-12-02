from fastapi import APIRouter, Depends
from app.services.metadata import get_all_jobs
from app.db.postgres import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_jobs(db=Depends(get_db)):
    return get_all_jobs(db)
