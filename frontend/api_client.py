import requests
from config import *

def upload_document(file):
    """Upload a document (resume) to the backend."""
    files = {"file": file}
    response = requests.post(UPLOAD_ENDPOINT, files=files)
    return response.json()

def query_rag(question, job_id):
    """Query the RAG system with a question and a specific job context."""
    try:
        payload = {"query": question, "job_id": str(job_id)}
        response = requests.post(QUERY_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e), "answer": "An error occurred while querying the system."}
    
def get_ats_score(job_id, jd_text):
    """
    Fetch ATS match score.
    JD Text is mandatory for this request.
    """
    try:
        payload = {
            "job_id": str(job_id), 
            "job_description": jd_text
        }
        response = requests.post(SCORE_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching ATS score: {e}")
        return {"error": str(e)}