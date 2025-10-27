"""
AI Legal Aid Assistant - Simple, Fast, Working Version
No disclaimer, fast loading, reliable responses
"""

import os
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['USE_TORCH'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import streamlit as st
import time
from pathlib import Path
import traceback
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Legal Rights Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Common Questions Section */
    .common-questions {
        margin: 2rem 0;
        padding: 1.5rem;
        background: #f8fafc;
        border-radius: 12px;
        border-left: 4px solid #4f46e5;
        color: #000000 !important;  /* Force black text color */
    }
    
    .common-questions h3 {
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .question-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .question-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .question-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
        border-color: #c7d2fe;
    }
    
    .question-card h4 {
        color: #1e40af;  /* Darker blue for better contrast */
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }
    
    .question-card p {
        color: #1f2937;  /* Dark gray for better readability */
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.5;
    }
    
    .common-questions h3 {
        color: #1e40af !important;  /* Dark blue for heading */
        margin-bottom: 1rem !important;
    }
    
    .common-questions {
        color: #1f2937 !important;  /* Dark gray for all text in the section */
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Chat Messages */
    .message {
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        max-width: 85%;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .assistant-message {
        background: white;
        border: 2px solid #e2e8f0;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        color: #2d3748;
    }
    
    .message-header {
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .message-content {
        line-height: 1.7;
        white-space: pre-wrap;
    }
    
    /* Suggested Questions */
    .suggested-questions {
        margin: 2rem 0;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 12px;
        border-left: 4px solid #667eea;
    }
    
    .suggested-questions h4 {
        color: #4a5568;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .suggested-questions .question-chip {
        display: inline-block;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .suggested-questions .question-chip:hover {
        background: #f0f4f8;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    }
    
    /* Source Cards */
    .source-card {
        background: #f8fafc;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.75rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .source-title {
        font-weight: 600;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .source-text {
        color: #4a5568;
        font-size: 0.9rem;
        font-style: italic;
    }
    
    /* Input */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Suggested Questions */
    .suggested-btn {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'rag_initialized' not in st.session_state:
        st.session_state.rag_initialized = False
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None


def load_rag_pipeline_safe():
    """Load RAG pipeline - using the original working version"""
    try:
        from rag_pipeline import RAGPipeline
        
        rag = RAGPipeline(
            data_dir="data",
            db_dir="db",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            llm_model="google/flan-t5-small"  # Using small for speed
        )
        
        doc_count = rag.collection.count()
        if doc_count == 0:
            num_chunks = rag.ingest_pdfs()
            return rag, None, num_chunks
        
        return rag, None, doc_count
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        return None, error_msg, 0


def _format_answer(self, answer):
    """Format the answer with proper structure and formatting"""
    # Split into sentences for better formatting
    sentences = [s.strip() for s in answer.split('. ') if s.strip()]
    
    # Ensure minimum number of sentences
    if len(sentences) < 5:  # If answer is too short, add more context
        return answer + "\n\nFor more specific information, please provide additional details about your situation."
    
    # Format with paragraphs and bullet points for better readability
    formatted = []
    formatted.append(sentences[0] + ".")  # Main point
    
    if len(sentences) > 1:
        formatted.append("\n" + sentences[1] + ".")  # Explanation
    
    if len(sentences) > 2:
        # Key points as bullet points
        formatted.append("\nKey points to consider:")
        for point in sentences[2:min(6, len(sentences))]:  # Up to 4 key points
            formatted.append(f"• {point}.")
    
    if len(sentences) > 6:
        formatted.append("\n" + ". ".join(sentences[6:]) + ".")  # Additional details
    
    return "\n".join(formatted)

def display_message(role, content, sources=None):
    """Display a chat message with enhanced formatting"""
    if role == "user":
        st.markdown(f"""
        <div class="message user-message">
            <div class="message-header">👤 You</div>
            <div class="message-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Split content into paragraphs for better readability
        paragraphs = content.split('\n\n')
        formatted_content = ""
        
        for para in paragraphs:
            if para.startswith('•'):
                # Format bullet points
                formatted_content += f'<div style="margin: 0.5rem 0 0.5rem 1rem; line-height: 1.6;">{para}</div>'
            elif para.lower().startswith(('key points', 'important', 'note')):
                # Format headings
                formatted_content += f'<div style="font-weight: 600; margin: 1rem 0 0.5rem 0; color: #4f46e5;">{para}</div>'
            else:
                # Regular paragraph
                formatted_content += f'<div style="margin: 0.75rem 0;">{para}</div>'
        
        st.markdown(f"""
        <div class="message assistant-message">
            <div class="message-header">⚖️ Legal Assistant</div>
            <div class="message-content" style="line-height: 1.8;">
                {formatted_content}
                <div style="margin-top: 1rem; font-size: 0.9em; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 0.75rem;">
                    💡 <em>This information is for educational purposes only. For specific legal advice, please consult a qualified attorney.</em>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if sources and len(sources) > 0:
            with st.expander(f"📚 View {len(sources)} Source(s)", expanded=False):
                for i, source in enumerate(sources, 1):
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-title">
                            📄 Source {i}: {source.get('source', 'Document')} (Page {source.get('page', 'N/A')})
                        </div>
                        <div class="source-text">
                            "{source.get('snippet', '')}"
                        </div>
                        <div style="margin-top: 0.5rem; font-size: 0.85em; color: #64748b;">
                            Relevance: {source.get('score', 0):.2f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

def main():
    # Common legal questions
    COMMON_QUESTIONS = [
        "What are my rights if I'm arrested by the police?",
        "How can I file a consumer complaint in India?",
        "What are the rights of women against domestic violence?",
        "How to file an RTI application?",
        "What are the legal working hours in India?",
        "How to register a complaint about online fraud?",
        "What are the rights of tenants and landlords?",
        "How to get a legal heir certificate?",
        "What to do if your employer doesn't pay salary?",
        "How to file a cyber crime complaint?"
    ]
    
    # Display header
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">⚖️ Legal Rights Assistant</h1>
            <p class="hero-subtitle">Get clear, reliable information about your legal rights in India</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display suggested questions with better styling
    st.markdown(
        """
        <div style="margin: 2rem 0; padding: 1.5rem; background: #f8f9fa; border-radius: 12px; border-left: 4px solid #4f46e5;">
            <h4 style="color: #1e40af; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                🔍 Common Legal Questions:
            </h4>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
        """,
        unsafe_allow_html=True
    )
    
    # Add each question as a separate markdown element
    for question in COMMON_QUESTIONS:
        # Escape single quotes in the question
        escaped_question = question.replace("'", "\\'")
        st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                cursor: pointer;
                color: #1f2937;
                font-size: 0.9rem;
                transition: all 0.2s;"
                onmouseover="this.style.borderColor='#a5b4fc'; this.style.boxShadow='0 2px 8px rgba(99, 102, 241, 0.1)';"
                onmouseout="this.style.borderColor='#e2e8f0'; this.style.boxShadow='none';"
                onclick="document.getElementById('question-input').value='{escaped_question}'; document.querySelector('button[title=\"Send\"]').click();"
                onmousedown="this.style.transform='translateY(1px)';"
                onmouseup="this.style.transform='none';">
                {question}
            </div>
        """, unsafe_allow_html=True)
    
    # Close the container div
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)
def main():
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'rag_initialized' not in st.session_state:
        st.session_state.rag_initialized = False
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
        
    # Common legal questions - moved to top of function
    COMMON_QUESTIONS = [
        "What are my rights if I'm arrested by the police?",
        "How can I file a consumer complaint in India?",
        "What are the rights of women against domestic violence?",
        "How to file an RTI application?",
        "What are the legal working hours in India?",
        "How to register a complaint about online fraud?",
        "What are the rights of tenants and landlords?",
        "How to get a legal heir certificate?",
        "What to do if your employer doesn't pay salary?",
        "How to file a cyber crime complaint?"
    ]
    
    # Set up RAG pipeline with optimized parameters
    if not st.session_state.rag_initialized:
        with st.spinner("🚀 Loading AI models..."):
            try:
                from rag_pipeline import RAGPipeline
                st.session_state.rag_pipeline = RAGPipeline(
                    data_dir="data",
                    db_dir="db",
                    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
                    llm_model="google/flan-t5-base",
                    chunk_size=500,
                    chunk_overlap=50
                )
                st.session_state.rag_initialized = True
                st.rerun()
            except Exception as e:
                st.error(f"Error initializing AI models: {str(e)}")
    
    # Display header
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">⚖️ Legal Rights Assistant</h1>
            <p class="hero-subtitle">Get clear, reliable information about your legal rights in India</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display suggested questions with better styling
    st.markdown(
        """
        <div style="margin: 2rem 0; padding: 1.5rem; background: #f8f9fa; border-radius: 12px; border-left: 4px solid #4f46e5;">
            <h4 style="color: #1e40af; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                🔍 Common Legal Questions:
            </h4>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
        """,
        unsafe_allow_html=True
    )
    
    # Add each question as a separate markdown element
    for question in COMMON_QUESTIONS:
        # Escape single quotes in the question
        escaped_question = question.replace("'", "\\'")
        st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                cursor: pointer;
                color: #1f2937;
                font-size: 0.9rem;
                transition: all 0.2s;"
                onmouseover="this.style.borderColor='#a5b4fc'; this.style.boxShadow='0 2px 8px rgba(99, 102, 241, 0.1)';"
                onmouseout="this.style.borderColor='#e2e8f0'; this.style.boxShadow='none';"
                onclick="document.getElementById('question-input').value='{escaped_question}'; document.querySelector('button[title=\"Send\"]').click();"
                onmousedown="this.style.transform='translateY(1px)';"
                onmouseup="this.style.transform='none';">
                {question}
            </div>
        """, unsafe_allow_html=True)
    
    # Close the container div
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📚 Knowledge Base")
        
        data_dir = Path("data")
        if data_dir.exists():
            pdf_files = list(data_dir.glob("*.pdf"))
            st.markdown(f"**{len(pdf_files)} Documents Loaded**")
            for pdf in pdf_files:
                st.markdown(f"✓ {pdf.stem}")
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        top_k = st.slider("Number of sources", 1, 5, 3)
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.info("Ask specific questions about your legal rights for best results.")
    
    # Initialize RAG
    if not st.session_state.rag_initialized:
        with st.spinner("🚀 Loading AI models..."):
            rag, error, count = load_rag_pipeline_safe()
            
            if error:
                st.error(f"❌ Failed to load: {error}")
                st.info("💡 Try restarting the app or check if PDF files are in the 'data' folder.")
                st.stop()
            else:
                st.session_state.rag_pipeline = rag
                st.session_state.rag_initialized = True
                st.success(f"✅ Ready! {count} text chunks loaded")
                time.sleep(1)
                st.rerun()
    
    # Chat Interface
    st.markdown("### 💬 Ask Your Question")
    
    # Display messages
    for msg in st.session_state.messages:
        display_message(msg['role'], msg['content'], msg.get('sources'))
    
    # Input area
    prompt = st.chat_input("Ask me about your legal rights...", key="question-input")
    
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        display_message("user", prompt)
        
        # Add a placeholder for the assistant's response
        response_placeholder = st.empty()
        
        # Generate response with streaming effect
        with st.spinner("Analyzing your question..."):
            try:
                # Get response from RAG pipeline with optimized parameters
                response = st.session_state.rag_pipeline.query(
                    question=prompt,
                    top_k=top_k
                )
                
                # Get the answer with fallback
                answer = response.get('answer', 'I apologize, but I could not generate a response. Please try again.')
                
                # Display response with typing effect
                full_response = ""
                message_placeholder = st.empty()
                
                # Stream the response with a faster typing effect
                for word in answer.split():
                    full_response += word + " "
                    if len(full_response) % 10 == 0:  # Update every 10 characters for better performance
                        message_placeholder.markdown(
                            f'<div class="message assistant-message">'
                            f'<div class="message-header">⚖️ Legal Assistant</div>'
                            f'<div class="message-content">{full_response}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    time.sleep(0.015)  # Slightly faster typing effect
                
                # Add to chat history with formatted answer
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': answer,
                    'sources': response.get('sources', []),
                    'timestamp': datetime.now().isoformat()
                })
                
                # Display sources if available
                sources = response.get('sources', [])
                if sources:
                    with st.expander(f"📚 View {len(sources)} Source(s)", expanded=False):
                        for i, source in enumerate(sources, 1):
                            st.markdown(
                                f'<div class="source-card">'
                                f'<div class="source-title">Source {i}: {source.get("source", "Document")}</div>'
                                f'<div class="source-text">{source.get("snippet", "")}</div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )
                
            except Exception as e:
                error_msg = f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question or try again later."
                st.error("An error occurred while processing your request.")
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': error_msg,
                    'timestamp': datetime.now().isoformat()
                })
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #718096; padding: 1rem;'>
        <small>Legal Rights Assistant • Educational Tool</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
