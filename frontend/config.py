# Streamlit Configuration

BACKEND_URL = "http://localhost:8000"   # FastAPI backend
UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload/"  
QUERY_ENDPOINT = f"{BACKEND_URL}/query/"    
LIST_DOCS_ENDPOINT = f"{BACKEND_URL}/jobs/" 
SCORE_ENDPOINT = f"{BACKEND_URL}/score/"