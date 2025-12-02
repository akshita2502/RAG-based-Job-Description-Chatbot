from sqlalchemy.orm import Session
from app.models.models import Job

def save_job(db: Session, title: str, filename: str):
    job = Job(title=title, filename=filename)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()

def get_all_jobs(db: Session):
    return db.query(Job).all()
