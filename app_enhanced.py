"""
AI Legal Aid Assistant - Enhanced Professional Interface
A social welfare web application to educate people about their legal rights
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
    page_title="Legal Rights Education Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': """
        # Legal Rights Education Platform
        
        **Mission:** Empowering citizens with knowledge of their legal rights.
        
        This platform helps students, workers, consumers, and all citizens understand 
        their fundamental rights and legal protections in India.
        
        **Disclaimer:** This is an educational tool. For legal advice, consult a qualified attorney.
        """
    }
)

# Enhanced Professional CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Base styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #1a202c;
    }
    
    /* Header Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
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
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.95;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    .hero-mission {
        margin-top: 1.5rem;
        padding: 1rem 2rem;
        background: rgba(255,255,255,0.15);
        border-radius: 10px;
        backdrop-filter: blur(10px);
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Disclaimer Box - FIXED VISIBILITY WITH IMPORTANT */
    .disclaimer-box {
        background: linear-gradient(135deg, #fff5e6 0%, #ffe4cc 100%) !important;
        border: 3px solid #ff9800 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 2rem 0 !important;
        box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3) !important;
    }
    
    .disclaimer-title {
        display: flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #d84315 !important;
        margin-bottom: 1rem !important;
    }
    
    .disclaimer-content {
        color: #3e2723 !important;
        line-height: 1.8 !important;
        font-size: 1rem !important;
    }
    
    .disclaimer-content p {
        color: #3e2723 !important;
        margin-bottom: 0.75rem !important;
    }
    
    .disclaimer-content strong {
        color: #bf360c !important;
        font-weight: 700 !important;
    }
    
    /* Chat Container */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Message Bubbles */
    .message {
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        max-width: 80%;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
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
        font-size: 1rem;
    }
    
    /* Source Cards */
    .source-card {
        background: #f8fafc;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.75rem 0;
        border-radius: 0 8px 8px 0;
        transition: all 0.2s;
    }
    
    .source-card:hover {
        background: #edf2f7;
        transform: translateX(4px);
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
    
    /* Input Area */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        transition: all 0.2s;
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
        font-size: 1rem;
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
        display: inline-block;
        color: #4a5568;
        font-weight: 500;
    }
    
    .suggested-btn:hover {
        border-color: #667eea;
        background: #f7fafc;
        transform: translateY(-2px);
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .loading-dot {
        width: 12px;
        height: 12px;
        margin: 0 6px;
        background: #667eea;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: white;
    }
    
    /* Info Cards */
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    
    .info-card-title {
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .info-card-content {
        color: #4a5568;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #718096;
        border-top: 2px solid #e2e8f0;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title { font-size: 1.75rem; }
        .hero-subtitle { font-size: 1rem; }
        .message { max-width: 95%; }
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'rag_initialized' not in st.session_state:
        st.session_state.rag_initialized = False
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""


def load_rag_pipeline_safe():
    """Safely load RAG pipeline with error handling"""
    try:
        from rag_pipeline import RAGPipeline
        
        rag = RAGPipeline(
            data_dir="data",
            db_dir="db",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            llm_model="google/flan-t5-base"  # Using base model for better responses
        )
        
        # Check if we need to ingest
        doc_count = rag.collection.count()
        if doc_count == 0:
            num_chunks = rag.ingest_pdfs()
            return rag, None, num_chunks
        
        return rag, None, doc_count
        
    except Exception as e:
        error_msg = f"Error initializing system: {str(e)}\n\n{traceback.format_exc()}"
        return None, error_msg, 0


def display_message(role, content, sources=None):
    """Display a chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="message user-message">
            <div class="message-header">
                <span>👤</span> You
            </div>
            <div class="message-content">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message assistant-message">
            <div class="message-header">
                <span>⚖️</span> Legal Rights Assistant
            </div>
            <div class="message-content">{content}</div>
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
                    </div>
                    """, unsafe_allow_html=True)


def main():
    """Main application"""
    
    initialize_session_state()
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">⚖️ Legal Rights Education Platform</div>
        <div class="hero-subtitle">
            Empowering Students, Workers, and Citizens with Knowledge of Their Legal Rights
        </div>
        <div class="hero-mission">
            🎯 Our Mission: Bridge the gap between legal ignorance and awareness. 
            Understand your rights as a worker, consumer, student, and citizen of India.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer - MAXIMUM VISIBILITY WITH INLINE STYLES
    st.markdown("""
    <div class="disclaimer-box" style="background: linear-gradient(135deg, #fff5e6 0%, #ffe4cc 100%); 
         border: 3px solid #ff9800; border-radius: 12px; padding: 1.5rem; margin: 2rem 0; 
         box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);">
        <div class="disclaimer-title" style="display: flex; align-items: center; gap: 0.75rem; 
             font-size: 1.2rem; font-weight: 700; color: #d84315; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem;">⚠️</span>
            <span style="color: #d84315;">Important Legal Disclaimer</span>
        </div>
        <div class="disclaimer-content" style="color: #3e2723; line-height: 1.8; font-size: 1rem;">
            <p style="color: #3e2723; margin-bottom: 0.75rem;">
                <strong style="color: #bf360c; font-weight: 700;">Educational Purpose Only:</strong> 
                <span style="color: #3e2723;">This platform provides general legal information 
                to help you understand your rights. <strong style="color: #bf360c;">It is NOT a substitute for professional legal advice.</strong></span>
            </p>
            
            <p style="color: #3e2723; margin-top: 0.75rem; margin-bottom: 0.75rem;">
                <strong style="color: #bf360c; font-weight: 700;">Please Note:</strong> 
                <span style="color: #3e2723;">Laws and regulations change frequently. The information provided may not be complete, current, or applicable to your specific situation.</span>
            </p>
            
            <p style="color: #3e2723; margin-top: 0.75rem;">
                <strong style="color: #bf360c; font-weight: 700;">Action Required:</strong> 
                <span style="color: #3e2723;">For specific legal matters, disputes, or advice, always consult with a qualified legal professional or official authority.</span>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #667eea; margin-bottom: 0.5rem;">📚 Knowledge Base</h2>
            <p style="color: #718096; font-size: 0.9rem;">Official legal documents</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show loaded documents
        data_dir = Path("data")
        if data_dir.exists():
            pdf_files = list(data_dir.glob("*.pdf"))
            st.markdown(f"**{len(pdf_files)} Documents:**")
            for pdf in pdf_files:
                st.markdown(f"✓ {pdf.stem}")
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        top_k = st.slider("Sources per answer", 1, 5, 3,
                         help="More sources = more comprehensive answers")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Info Card
        st.markdown("""
        <div class="info-card">
            <div class="info-card-title">💡 How to Use</div>
            <div class="info-card-content">
                1. Type your question below<br>
                2. Click Send or press Enter<br>
                3. View sources for verification<br>
                4. Ask follow-up questions
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize RAG
    if not st.session_state.rag_initialized:
        with st.status("🚀 Initializing Legal Knowledge System...", expanded=True) as status:
            st.write("Loading AI models and legal documents...")
            rag, error, count = load_rag_pipeline_safe()
            
            if error:
                status.update(label="❌ Initialization Failed", state="error")
                st.error(f"Error: {error}")
                st.stop()
            else:
                st.session_state.rag_pipeline = rag
                st.session_state.rag_initialized = True
                status.update(label=f"✅ Ready! {count} legal text chunks loaded", state="complete")
                time.sleep(1)
                st.rerun()
    
    # Chat Interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown("### 💬 Ask About Your Legal Rights")
    
    # Display chat history
    for msg in st.session_state.messages:
        display_message(msg['role'], msg['content'], msg.get('sources'))
    
    # Suggested Questions
    if len(st.session_state.messages) == 0:
        st.markdown("#### 💡 Try asking:")
        cols = st.columns(2)
        
        questions = [
            "What are the basic rights of workers in India?",
            "How can I file a consumer complaint?",
            "What is the minimum wage law?",
            "What are my digital privacy rights?"
        ]
        
        for i, q in enumerate(questions):
            with cols[i % 2]:
                if st.button(q, key=f"suggest_{i}", use_container_width=True):
                    st.session_state.current_question = q
                    st.rerun()
    
    st.markdown("---")
    
    # Input Area
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_question = st.text_input(
            "Your question:",
            value=st.session_state.current_question,
            placeholder="e.g., What are my rights as a student?",
            key="question_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_clicked = st.button("Send", type="primary", use_container_width=True)
    
    # Handle question submission
    if send_clicked and user_question:
        # Clear the current question
        st.session_state.current_question = ""
        
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_question,
            'timestamp': datetime.now().isoformat()
        })
        
        # Get AI response
        try:
            with st.spinner("🤔 Analyzing legal documents..."):
                result = st.session_state.rag_pipeline.query(user_question, top_k=top_k)
                
                # Add assistant response
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': result['answer'],
                    'sources': result.get('sources', []),
                    'timestamp': datetime.now().isoformat()
                })
                
        except Exception as e:
            st.error(f"⚠️ Error generating response: {str(e)}")
            st.session_state.messages.append({
                'role': 'assistant',
                'content': "I apologize, but I encountered an error while processing your question. Please try rephrasing or ask another question.",
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
            Legal Rights Education Platform
        </div>
        <div style="font-size: 0.9rem; color: #a0aec0;">
            Empowering citizens through legal knowledge • A social welfare initiative
        </div>
        <div style="margin-top: 1rem; font-size: 0.85rem;">
            Built with ❤️ using Streamlit, HuggingFace, ChromaDB & Sentence Transformers
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
