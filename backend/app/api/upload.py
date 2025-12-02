from typing import Optional
from fastapi import APIRouter, UploadFile, Depends
from app.services.file_parser import extract_text
from app.services.ingestion import ingest_document
from app.services.metadata import save_job
from app.db.postgres import SessionLocal
from app.core.config import settings

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def upload_jd(title: Optional[str] = None, file: Optional[UploadFile] = None, db=Depends(get_db)):
    if not file:
        return {"error": "No file provided"}
    
    if not file.filename:
        return {"error": "No file provided"}
    
    # Use filename as title if title is not provided
    job_title = title or file.filename.replace(".pdf", "").replace(".docx", "")
    
    filepath = f"{settings.UPLOAD_DIR}/{file.filename}"
    
    with open(filepath, "wb") as f:
        f.write(await file.read())

    text = extract_text(filepath)

    job = save_job(db, job_title, file.filename)

    chunks = ingest_document(str(job.id), text)

    return {"job_id": job.id, "chunks_stored": chunks}
