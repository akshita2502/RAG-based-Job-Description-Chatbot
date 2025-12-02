# backend/app/services/rag_search.py
from typing import Optional, Any
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from app.core.config import settings

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma = PersistentClient(path=settings.CHROMA_PATH)
collection = chroma.get_or_create_collection(name="job_docs")

def rag_retrieve(query: str, job_id: Optional[str] = None):
    """Retrieve relevant documents for a query, optionally filtering by job_id."""
    query_emb = model.encode(query, convert_to_numpy=True).tolist()

    # Define filter if job_id is provided
    # Chroma expects None for no filter or a proper Where clause
    where_filter: Any = None
    if job_id:
        where_filter = {"job_id": job_id}

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=3,
        where=where_filter  # <--- CRITICAL ADDITION: This ensures we only search the current resume
    )

    docs = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
    
    return docs