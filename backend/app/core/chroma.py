import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings

chroma_client = chromadb.Client(
    ChromaSettings(chroma_db_impl="duckdb+parquet", persist_directory=settings.CHROMA_PATH)
)

# Ensure collection exists
collection = chroma_client.get_or_create_collection(
    "job_descriptions",
    metadata={"hnsw:space": "cosine"}
)
