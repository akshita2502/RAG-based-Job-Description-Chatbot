# frontend/app.py
import streamlit as st
from api_client import upload_document, query_rag

# --- Page Config ---
st.set_page_config(
    page_title="Resume Chatbot",
    page_icon="📄",
    layout="centered"
)

# --- Custom CSS for "Clean" Look ---
st.markdown("""
<style>
    .main {
        background-color: #f9f9f9;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    .uploadedFile {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 10px;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "current_job_id" not in st.session_state:
    st.session_state.current_job_id = None
if "current_filename" not in st.session_state:
    st.session_state.current_filename = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Header ---
st.title("📄 AI Resume Chatbot")
st.caption("Upload a resume and ask questions specifically about it.")

# --- 1. Upload Section ---
with st.container():
    uploaded_file = st.file_uploader("Upload a Resume (PDF/DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

    if uploaded_file:
        # Check if this is a NEW file upload
        if st.session_state.current_filename != uploaded_file.name:
            with st.spinner("Processing new document..."):
                result = upload_document(uploaded_file)
                
                if "job_id" in result:
                    # New context established!
                    st.session_state.current_job_id = result["job_id"]
                    st.session_state.current_filename = uploaded_file.name
                    
                    # CLEAR previous chat history because context has changed
                    st.session_state.messages = [] 
                    
                    st.success(f"✅ Loaded: {uploaded_file.name}")
                else:
                    st.error("Failed to process document.")

# --- 2. Chat Interface ---
# Only show chat if a document is successfully loaded
if st.session_state.current_job_id:
    st.divider()
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input(f"Ask about {st.session_state.current_filename}..."):
        # 1. Add user message to state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Get Answer from Backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = query_rag(prompt, st.session_state.current_job_id)
                answer = response.get("answer", "I couldn't get an answer.")
                
            st.markdown(answer)
            
        # 3. Add assistant response to state
        st.session_state.messages.append({"role": "assistant", "content": answer})

else:
    # Placeholder when no file is uploaded
    st.info("👆 Please upload a document to start chatting.")