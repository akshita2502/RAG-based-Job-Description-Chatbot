from app.services.rag_search import rag_retrieve
from app.core.gemini_client import gemini_client

def chat_with_jd(query: str, job_id: str):
    # Retrieve relevant chunks for this specific resume
    retrieved_docs = rag_retrieve(query, job_id=job_id)
    
    context = "\n\n".join(retrieved_docs)

    # UPDATED PROMPT: Tailored for ATS Best Practices
    prompt = f"""
    You are an expert Career Coach and ATS (Applicant Tracking System) Specialist. 
    You are analyzing a resume text to help the candidate optimize it for automated screening systems.

    RESUME CONTEXT (Extracted Text):
    {context}

    USER QUERY:
    {query}

    INSTRUCTIONS:
    1. **Factual Questions:** If the user asks for specific details (e.g., "What is my phone number?", "Did I list Python?"), answer strictly using the provided RESUME CONTEXT.
    
    2. **Evaluative/Advice Questions:** If the user asks for feedback, ratings, or improvements (e.g., "Is this ATS friendly?", "Rate my resume"), evaluate the content based on these ATS Best Practices:
       - **Keywords:** Are standard industry terms used? (e.g., "Python" vs "Coding in Py").
       - **Quantifiable Metrics:** Does the resume use numbers to measure success? (e.g., "Increased sales by 20%").
       - **Standard Headings:** Are sections clearly labeled (Experience, Education, Skills)?
       - **Formatting:** Warn against columns, graphics, or complex tables if the text structure implies them.
       - **Action Verbs:** Does it start bullet points with strong verbs (Led, Developed, Optimized)?

    3. **Tone:** Be encouraging but direct about missing critical elements. 
    """

    answer = gemini_client.generate_answer(prompt)
    return answer