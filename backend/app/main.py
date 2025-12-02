from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import upload, query, jobs, health

app = FastAPI(title="RAG Job Description Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(query.router, prefix="/query", tags=["Chat"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/")
def root():
    return {"message": "RAG Job Description Chatbot Backend Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
