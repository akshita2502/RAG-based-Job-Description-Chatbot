# # Streamlit Configuration

# BACKEND_URL = "http://localhost:8000"   # FastAPI backend
# UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload"
# QUERY_ENDPOINT = f"{BACKEND_URL}/query"
# LIST_DOCS_ENDPOINT = f"{BACKEND_URL}/jobs"

# Streamlit Configuration

BACKEND_URL = "http://localhost:8000"   # FastAPI backend
UPLOAD_ENDPOINT = f"{BACKEND_URL}/upload/"  # Added trailing slash
QUERY_ENDPOINT = f"{BACKEND_URL}/query/"    # Added trailing slash
LIST_DOCS_ENDPOINT = f"{BACKEND_URL}/jobs/" # Added trailing slash