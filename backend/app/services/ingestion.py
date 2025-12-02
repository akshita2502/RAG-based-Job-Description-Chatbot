# backend/app/services/ingestion.py
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from app.core.config import settings

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma = PersistentClient(path=settings.CHROMA_PATH)
collection = chroma.get_or_create_collection(name="job_docs")

def ingest_document(doc_id: str, text: str):
    # Create embedding
    embedding = model.encode(text, convert_to_numpy=True).tolist()

    # Store text, embedding, AND metadata (job_id)
    collection.upsert(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[{"job_id": doc_id}]  # <--- CRITICAL ADDITION
    )
    return True