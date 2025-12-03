import json
from sentence_transformers import SentenceTransformer, util
from app.services.rag_search import get_document_text
from app.core.gemini_client import gemini_client

# Load the embedding model once to be reused across requests
similarity_model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_ats_score(job_id: str, job_description: str):
    """
    Calculates a match score between a specific resume (job_id) and a provided Job Description.
    """
    
    # 1. Validate Inputs
    if not job_description:
        return {"error": "Job description is required for this analysis."}

    resume_text = get_document_text(job_id)
    if not resume_text:
        return {"error": "Resume text not found in database."}

    # 2. Calculate Mathematical Match Score (Vector Similarity)
    # This gives us a grounded "base score" (0-100) based on semantic similarity
    resume_emb = similarity_model.encode(resume_text, convert_to_tensor=True)
    jd_emb = similarity_model.encode(job_description, convert_to_tensor=True)
    
    # Calculate cosine similarity (returns 0.0 to 1.0)
    similarity = util.cos_sim(resume_emb, jd_emb).item()
    match_score = round(similarity * 100, 1)

    # 3. AI Qualitative Analysis
    # We feed the math score into the prompt so the AI can explain "why" the score is what it is.
    prompt = f"""
    Act as an expert ATS (Applicant Tracking System) Scanner. 
    Compare the candidate's Resume against the provided Job Description.
    
    RESUME TEXT: 
    {resume_text[:10000]}
    
    JOB DESCRIPTION: 
    {job_description[:5000]}
    
    CALCULATED MATCH SCORE: {match_score}%
    
    TASK:
    1. Identify 3-5 critical Hard Skills or Keywords from the JD that are MISSING in the Resume.
    2. Provide a concrete recommendation on how to improve the resume for THIS specific role.
    3. Provide a 1-sentence summary of the candidate's fit.

    OUTPUT FORMAT:
    Return ONLY a valid JSON object. No markdown.
    {{
        "match_score": {match_score},
        "missing_keywords": ["Skill1", "Skill2", ...],
        "recommendation": "Advice on tailoring...",
        "summary": "Brief summary..."
    }}
    """

    try:
        response_text = gemini_client.generate_answer(prompt)
        
        # Clean response to ensure valid JSON
        cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_text)
        
    except Exception as e:
        print(f"Error analyzing ATS score: {e}")
        # Fallback: Return the calculated math score even if the AI explanation fails
        return {
            "match_score": match_score,
            "missing_keywords": ["Error analyzing keywords"],
            "recommendation": "Could not generate detailed advice, but the match score is accurate.",
            "summary": "Analysis interrupted."
        }
