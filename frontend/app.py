import streamlit as st
from api_client import upload_document, query_rag, get_ats_score

# --- Page Config ---
st.set_page_config(
    page_title="AI ATS Resume Checker",
    page_icon="✅",
    layout="wide"
)

# --- Custom CSS for Metrics ---
st.markdown("""
<style>
    .main { background-color: #f9f9f9; }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        text-align: center;
    }
    .score-high { color: green; font-weight: bold; }
    .score-med { color: orange; font-weight: bold; }
    .score-low { color: red; font-weight: bold; }
    .score-val { font-size: 3em; margin: 0; }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "current_job_id" not in st.session_state:
    st.session_state.current_job_id = None
if "current_filename" not in st.session_state:
    st.session_state.current_filename = None
if "ats_result" not in st.session_state:
    st.session_state.ats_result = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Header ---
st.title("✅ AI ATS Resume Checker")
st.caption("Upload your resume and provide a Job Description to check your compatibility.")

# --- 1. Upload Section ---
with st.container():
    uploaded_file = st.file_uploader("1. Upload Resume (PDF/DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

    if uploaded_file:
        # Trigger processing only if it's a new file
        if st.session_state.current_filename != uploaded_file.name:
            with st.spinner("Processing document..."):
                result = upload_document(uploaded_file)
                
                if "job_id" in result:
                    st.session_state.current_job_id = result["job_id"]
                    st.session_state.current_filename = uploaded_file.name
                    st.session_state.messages = []
                    st.session_state.ats_result = None # Reset score on new file
                    
                    # FIX 1: Removed 'get_ats_score' call here. 
                    # We wait for the user to provide the JD in Section 2.
                    st.success(f"✅ Loaded: {uploaded_file.name}")
                else:
                    st.error("Upload failed. Please try again.")

# --- 2. JD Input & Analysis ---
if st.session_state.current_job_id:
    st.divider()
    
    col_input, col_btn = st.columns([4, 1])
    
    with col_input:
        jd_text = st.text_area("2. Paste Job Description (Required for scoring)", height=150)
        
    with col_btn:
        st.write("") # Spacer
        st.write("") # Spacer
        if st.button("📊 Calculate Score", type="primary", use_container_width=True):
            if not jd_text.strip():
                st.warning("⚠️ Job Description is required.")
            else:
                with st.spinner("Analyzing match..."):
                    # This call is correct because we now have the jd_text
                    st.session_state.ats_result = get_ats_score(st.session_state.current_job_id, jd_text)

# --- 3. Display Results ---
if st.session_state.ats_result:
    res = st.session_state.ats_result
    
    # Handle API errors gracefully
    if "error" in res:
        st.error(f"Analysis Failed: {res['error']}")
    else:
        st.divider()
        st.subheader("📊 Match Analysis Report")
        
        # Feature 1: Resume Scoring
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            # FIX 2: Explicitly cast score to int to fix the "Operator < not supported" error
            try:
                score = int(res.get("match_score", 0))
            except (ValueError, TypeError):
                score = 0
            
            # Now we can safely compare integers
            if score >= 75:
                score_class = "score-high"
            elif score >= 50:
                score_class = "score-med"
            else:
                score_class = "score-low"
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>Match Score</h3>
                <h1 class="{score_class} score-val">{score}%</h1>
            </div>
            """, unsafe_allow_html=True)

        # Feature 2 & 4: Recommendations & Missing Keywords
        with col2:
            st.markdown("""<div class="metric-card" style="text-align:left;"><h4>🔍 Missing Keywords</h4>""", unsafe_allow_html=True)
            keywords = res.get("missing_keywords", [])
            if not keywords:
                st.success("All key terms found!")
            else:
                for k in keywords:
                    st.markdown(f"• {k}")
            st.markdown("</div>", unsafe_allow_html=True)