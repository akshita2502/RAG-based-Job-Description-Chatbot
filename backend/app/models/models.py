from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.postgres import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
