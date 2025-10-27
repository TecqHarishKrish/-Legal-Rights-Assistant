"""
AI Legal Aid Chatbot - Enhanced Interface
Modern, accessible, and user-friendly legal aid assistant
"""

import os
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['USE_TORCH'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import streamlit as st
import time
from pathlib import Path
import traceback
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Legal Aid Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://example.com/help',
        'Report a bug': 'https://example.com/bug',
        'About': "# AI Legal Aid Assistant\n\nA tool to help you understand your legal rights."
    }
)

# Enhanced CSS with modern design
st.markdown("""
<style>
    /* Base styles */
    .main {
        background-color: #f8fafc;
        color: #1e293b;
        line-height: 1.6;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Message bubbles */
    .message {
        padding: 1.25rem 1.5rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        max-width: 85%;
        position: relative;
        line-height: 1.6;
        animation: fadeIn 0.3s ease-out;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.2s ease;
    }
    
    .message:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
        margin-right: 1rem;
    }
    
    .bot-message {
        background: white;
        border: 1px solid #e2e8f0;
        margin-right: auto;
        margin-left: 1rem;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    
    /* Better spacing for markdown content */
    .markdown-content {
        line-height: 1.7;
    }
    
    .markdown-content p {
        margin-bottom: 1em;
    }
    
    .markdown-content h3 {
        margin-top: 1.5em;
        margin-bottom: 0.75em;
        color: #1e293b;
        font-weight: 600;
    }
    
    .markdown-content ul, .markdown-content ol {
        margin-top: 0.5em;
        margin-bottom: 1em;
        padding-left: 1.5em;
    }
    
    .markdown-content li {
        margin-bottom: 0.5em;
    }
    
    /* Source cards */
    .source-card {
        background: #f8fafc;
        border-left: 3px solid #4f46e5;
        padding: 0.75rem 1rem;
        margin: 0.75rem 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.9em;
    }
    
    .source-title {
        font-weight: 600;
        color: #4f46e5;
        margin-bottom: 0.25rem;
    }
    
    .source-snippet {
        color: #64748b;
        font-style: italic;
        margin: 0.25rem 0;
    }
    
    .source-page {
        font-size: 0.85em;
        color: #94a3b8;
    }
    
    /* Input area */
    .stTextInput>div>div>input {
        border-radius: 24px;
        padding: 0.75rem 1.25rem;
        font-size: 1rem;
        border: 2px solid #e2e8f0;
        transition: all 0.2s;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 24px;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    /* Header */
    .header-container {
        text-align: center;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .header-title {
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* Disclaimer */
    .disclaimer {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        font-size: 0.95em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #5a4a0a;
    }
    
    .disclaimer-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 700;
        color: #9a3412;
        margin-bottom: 0.75rem;
        font-size: 1.05em;
    }
    
    .disclaimer-title span {
        font-size: 1.5em;
    }
    
    /* Suggested questions */
    .suggested-questions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin: 1rem 0 1.5rem;
    }
    
    .suggested-question {
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-size: 0.9em;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .suggested-question:hover {
        background: #e2e8f0;
        transform: translateY(-1px);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .message {
            max-width: 90%;
        }
        
        .header-title {
            font-size: 1.75rem;
        }
        
        .header-subtitle {
            font-size: 1rem;
        }
    }
    
    /* Markdown content */
    .markdown-content h3 {
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        color: #1e293b;
    }
    
    .markdown-content ul, .markdown-content ol {
        padding-left: 1.5rem;
        margin: 0.75rem 0;
    }
    
    .markdown-content li {
        margin-bottom: 0.5rem;
    }
    
    .markdown-content strong {
        color: #1e293b;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading-dots {
        display: flex;
        gap: 0.25rem;
        padding: 1rem 0;
    }
    
    .loading-dot {
        width: 8px;
        height: 8px;
        background-color: #94a3b8;
        border-radius: 50%;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .loading-dot:nth-child(2) { animation-delay: 0.2s; }
    .loading-dot:nth-child(3) { animation-delay: 0.4s; }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: #64748b;
        font-size: 0.9em;
        border-top: 1px solid #e2e8f0;
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
    if 'sources_expanded' not in st.session_state:
        st.session_state.sources_expanded = {}
    if 'suggested_questions' not in st.session_state:
        st.session_state.suggested_questions = [
            "What are the basic rights of workers in India?",
            "How can I file a consumer complaint?",
            "What is the minimum wage law?",
            "What are my digital privacy rights?"
        ]


def load_rag_pipeline_safe():
    """Safely load RAG pipeline with error handling"""
    try:
        from rag_pipeline import RAGPipeline
        
        with st.spinner("🔄 Loading AI models... This may take a minute..."):
            rag = RAGPipeline(
                data_dir="data",
                db_dir="db",
                embedding_model="sentence-transformers/all-MiniLM-L6-v2",
                llm_model="google/flan-t5-small"
            )
            
            # Check if we need to ingest
            doc_count = rag.collection.count()
            if doc_count == 0:
                with st.spinner("📚 Processing PDF documents... This will take 2-5 minutes..."):
                    num_chunks = rag.ingest_pdfs()
                    st.success(f"✅ Successfully processed {num_chunks} text chunks!")
            
            return rag, None
            
    except Exception as e:
        error_msg = f"Error initializing system: {str(e)}\n\n{traceback.format_exc()}"
        return None, error_msg


def render_markdown(content):
    """Render markdown content with proper styling"""
    # Split content into sections
    sections = content.split('###')
    
    # Process each section
    result = []
    for i, section in enumerate(sections):
        if not section.strip():
            continue
            
        # Add section header
        if i > 0:  # Skip the first section as it's before the first header
            result.append(f"### {section.strip()}")
        else:
            result.append(section.strip())
    
    return '\n\n'.join(result)


def display_chat_message(role, content, sources=None, message_id=None):
    """Display a chat message with proper formatting"""
    if role == "user":
        # Use columns to create a better layout for user messages
        col1, col2 = st.columns([1, 20])
        with col1:
            st.markdown("<div style='text-align: center; margin-top: 0.5rem;'>👤</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="message user-message">
                <div style="font-weight: 600; margin-bottom: 0.25rem;">You</div>
                <div>{content}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Generate a unique ID for this message if not provided
        if message_id is None:
            message_id = f"msg_{int(time.time())}"
        
        # Use columns for bot messages too
        col1, col2 = st.columns([1, 20])
        with col1:
            st.markdown("<div style='text-align: center; margin-top: 0.5rem;'>🤖</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="message bot-message">
                <div style="font-weight: 600; margin-bottom: 0.5rem; color: #4f46e5;">Legal Assistant</div>
                <div class="markdown-content">
                    {render_markdown(content)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display sources if available
            if sources:
                # Store expander state
                expander_key = f"expander_{message_id}"
                if expander_key not in st.session_state:
                    st.session_state[expander_key] = False
                
                # Toggle button for sources
                if st.button(f"📚 View Sources ({len(sources)})", 
                           key=f"btn_{message_id}",
                           help="Click to view sources",
                           type="secondary"):
                    st.session_state[expander_key] = not st.session_state[expander_key]
                    st.rerun()
                
                # Display sources if expanded
                if st.session_state[expander_key]:
                    st.markdown(
                        "<div style='margin-top: 1rem; margin-bottom: 1.5rem;'>"
                        "<div style='font-size: 0.9em; color: #64748b; margin-bottom: 0.5rem;'>"
                        "Sources used in this response:</div></div>", 
                        unsafe_allow_html=True
                    )
                    
                    for i, source in enumerate(sources, 1):
                        source_text = source.get('source', 'Document')
                        page_num = source.get('page', 'N/A')
                        snippet = source.get('snippet', '')
                        
                        st.markdown(f"""
                        <div class="source-card">
                            <div class="source-title">
                                <span style="color: #4f46e5;">🔗</span> Source {i}: {source_text} (Page {page_num})
                            </div>
                            <div class="source-snippet">
                                {snippet}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


def display_loading_animation():
    """Display a loading animation"""
    return st.markdown("""
    <div class="loading-dots">
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application"""
    
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h1 style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚖️ Legal Aid Assistant</h1>
            <p style="color: #64748b; font-size: 0.9rem;">Your personal guide to legal rights in India</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📚 Knowledge Base")
        data_dir = Path("data")
        if data_dir.exists():
            pdf_files = list(data_dir.glob("*.pdf"))
            st.markdown(f"**{len(pdf_files)} documents loaded:**")
            for pdf in pdf_files:
                st.markdown(f"- {pdf.stem}")
        else:
            st.warning("No documents found in the data directory.")
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        # Add a slider for number of sources
        top_k = st.slider("Number of sources to retrieve", 1, 5, 3,
                         help="Increase to get more comprehensive answers, decrease for faster responses")
        
        # Add a button to clear chat history
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Example Questions")
        
        # Display suggested questions as buttons
        for question in st.session_state.suggested_questions:
            if st.button(question, key=f"suggest_{question[:20]}", 
                        use_container_width=True, 
                        help=f"Ask: {question}"):
                st.session_state.user_input = question
        
        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.8rem; color: #64748b; margin-top: 2rem;">
            <p>This tool uses AI to provide legal information based on official documents.</p>
            <p>For specific legal advice, please consult a qualified professional.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">AI Legal Aid Assistant</h1>
        <p class="header-subtitle">Get accurate, source-based answers to your legal questions about Labour Laws, Consumer Rights & Digital Privacy</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer - Using st.container with a key to maintain state
    disclaimer_expanded = st.session_state.get('disclaimer_expanded', True)
    
    with st.expander("⚠️ Important Legal Disclaimer", expanded=disclaimer_expanded):
        st.markdown("""
        <div class="disclaimer">
            <div style="color: #9a3412; font-weight: 600; margin-bottom: 0.75rem; font-size: 1.05em;">
                ⚠️ Important Notice
            </div>
            <div style="color: #5a4a0a; line-height: 1.6;">
                <p>This chatbot provides general legal information based on the documents in its knowledge base. 
                <strong>It is not a substitute for professional legal advice.</strong></p>
                
                <p style="margin-top: 0.75rem;">
                <strong>Please note:</strong> The information provided may not be complete, accurate, or up-to-date. 
                Laws and regulations change frequently, and their application can vary widely based on the specific facts involved.</p>
                
                <p style="margin-top: 0.75rem; font-weight: 500;">
                For specific legal matters, always consult with a qualified legal professional or official authority.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Update the expanded state
        st.session_state.disclaimer_expanded = st.session_state.get(f"expanded_{hash('disclaimer')}", True)
    
    # Initialize RAG if needed
    if not st.session_state.rag_initialized:
        with st.status("🚀 Initializing AI Legal Aid System...", expanded=True) as status:
            st.write("Loading AI models and setting up the knowledge base...")
            rag, error = load_rag_pipeline_safe()
            
            if error:
                status.error(f"❌ Failed to initialize:\n\n```\n{error}\n```")
                st.stop()
            else:
                st.session_state.rag_pipeline = rag
                st.session_state.rag_initialized = True
                doc_count = rag.collection.count()
                status.success(f"✅ System ready! Knowledge base contains {doc_count} text chunks")
                time.sleep(1)
                st.rerun()
    
    # Chat interface container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        st.markdown("### 💬 Chat with Legal Assistant")
        
        # Display existing messages
        for i, msg in enumerate(st.session_state.messages):
            display_chat_message(
                role=msg['role'],
                content=msg['content'],
                sources=msg.get('sources'),
                message_id=f"msg_{i}"
            )
        
        # Display loading animation if processing
        if st.session_state.get('processing', False):
            display_loading_animation()
    
    # Input area (fixed at bottom)
    with st.container():
        st.markdown("---")
        
        # Suggested questions
        st.markdown("#### 💡 Try asking:")
        cols = st.columns(2)
        for i, question in enumerate(st.session_state.suggested_questions):
            with cols[i % 2]:
                if st.button(question, key=f"suggest2_{i}", use_container_width=True):
                    st.session_state.user_input = question
        
        # Chat input
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Ask your legal question:",
                placeholder="e.g., What are my rights as a worker in India?",
                key="user_input",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("Send", use_container_width=True, type="primary")
        
        # Handle message submission
        if send_button and user_input:
            # Add user message to chat
            st.session_state.messages.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            # Clear the input field
            if 'user_input' in st.session_state:
                del st.session_state.user_input
            
            # Set processing state and rerun
            st.session_state.processing = True
            st.rerun()
            
            try:
                # Get response from RAG pipeline
                with st.spinner("Analyzing your question..."):
                    result = st.session_state.rag_pipeline.query(user_input, top_k=top_k)
                    
                    # Add bot response to chat
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': result['answer'],
                        'sources': result['sources'],
                        'timestamp': datetime.now().isoformat()
                    })
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': f"I'm sorry, but I encountered an error while processing your request. Please try again later.",
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
            
            # Clear processing state
            st.session_state.processing = False
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <div>AI Legal Aid Assistant v2.0</div>
        <div style="margin-top: 0.5rem;">
            <small>Built with ❤️ using Streamlit, HuggingFace, ChromaDB & Sentence Transformers</small>
        </div>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 0.5rem;">
            <small>🔒 100% Offline</small>
            <small>•</small>
            <small>🎯 RAG-Powered</small>
            <small>•</small>
            <small>📚 Source-Grounded</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-scroll to bottom of chat
    st.markdown("""
    <script>
    // Auto-scroll to bottom of chat
    function scrollToBottom() {
        window.scrollTo(0, document.body.scrollHeight);
    }
    
    // Run on page load and after Streamlit updates
    window.onload = scrollToBottom;
    window.addEventListener('load', scrollToBottom);
    
    // Also run after Streamlit updates
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
