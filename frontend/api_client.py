# frontend/api_client.py
import requests
from config import *

def upload_document(file):
    files = {"file": file}
    response = requests.post(UPLOAD_ENDPOINT, files=files)
    return response.json()

def query_rag(question, job_id):
    """Query the RAG system with a question and a specific job context."""
    try:
        # Send both query and job_id
        payload = {"query": question, "job_id": str(job_id)}
        response = requests.post(QUERY_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e), "answer": "An error occurred while querying the system."}