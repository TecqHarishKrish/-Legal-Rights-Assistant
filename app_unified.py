"""
Unified Modern UI for AI Legal Aid Chatbot
Includes web search, conversation history, export, and enhanced features
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
import json

# Page config
st.set_page_config(
    page_title="AI Legal Rights Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    }
    
    .disclaimer-box {
        background: linear-gradient(135deg, #fff5e6 0%, #ffe4cc 100%) !important;
        border: 3px solid #ff9800 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 2rem 0 !important;
        box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3) !important;
    }
    
    .message {
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
    }
    
    .assistant-message {
        background: white;
        border: 2px solid #e2e8f0;
        color: #2d3748;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
        font-size: 16px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Fix button text in sidebar */
    [data-testid="stSidebar"] .stButton button {
        font-size: 14px !important;
        padding: 0.5rem 1rem !important;
        height: auto !important;
    }
    
    /* Fix export button */
    [data-testid="stDownloadButton"] button {
        font-size: 14px !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* Improve text readability */
    .message {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Fix disclaimer text */
    .disclaimer-box p {
        font-size: 16px !important;
        line-height: 1.8 !important;
    }
    
    /* Fix source text */
    [data-testid="baseButton-secondary"] {
        font-size: 14px;
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
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = f"conv_{int(time.time())}"


def load_rag_pipeline_safe():
    """Safely load RAG pipeline with error handling and memory management"""
    try:
        from rag_pipeline_advanced import AdvancedRAGPipeline
        
        # Use smaller model to avoid memory issues with better configuration
        try:
            rag = AdvancedRAGPipeline(
                data_dir="data",
                db_dir="db",
                embedding_model="sentence-transformers/all-MiniLM-L6-v2",
                llm_model="google/flan-t5-small",  # Using small model to prevent memory errors
                enable_web_search=False  # Disable web search by default to reduce memory
            )
        except Exception as memory_error:
            # Fallback: try without web search capabilities
            print(f"Warning: Initial load had issues: {memory_error}")
            rag = AdvancedRAGPipeline(
                data_dir="data",
                db_dir="db",
                embedding_model="sentence-transformers/all-MiniLM-L6-v2",
                llm_model="google/flan-t5-small",
                enable_web_search=False
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


def export_conversation():
    """Export conversation to JSON"""
    conversation = {
        'conversation_id': st.session_state.conversation_id,
        'timestamp': datetime.now().isoformat(),
        'messages': st.session_state.messages
    }
    return json.dumps(conversation, indent=2)


def display_message(role, content, sources=None, web_sources=None):
    """Display a chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="message user-message">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">👤 You</div>
            <div style="line-height: 1.7;">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message assistant-message">
            <div style="font-weight: 600; margin-bottom: 0.5rem; color: #667eea;">⚖️ Legal Rights Assistant</div>
            <div style="line-height: 1.7; color: #2d3748;">{content}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if sources and len(sources) > 0:
            with st.expander(f"📚 Local Sources ({len(sources)})"):
                for i, source in enumerate(sources, 1):
                    st.markdown(f"""
                    <div style="background: #f8fafc; border-left: 4px solid #667eea; padding: 1rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0;">
                        <div style="font-weight: 600; color: #667eea; margin-bottom: 0.5rem;">
                            📄 {source.get('source', 'Document')} (Page {source.get('page', 'N/A')})
                        </div>
                        <div style="color: #4a5568; font-style: italic; font-size: 0.9rem;">
                            "{source.get('snippet', '')}"
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        if web_sources and len(web_sources) > 0:
            with st.expander(f"🌐 Web Sources ({len(web_sources)})"):
                for i, source in enumerate(web_sources, 1):
                    st.markdown(f"""
                    <div style="background: #f8fafc; border-left: 4px solid #10b981; padding: 1rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0;">
                        <div style="font-weight: 600; color: #10b981; margin-bottom: 0.5rem;">
                            🌐 {source.get('source', 'Web Source')}
                        </div>
                        <div style="color: #4a5568; font-style: italic; font-size: 0.9rem;">
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
        <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            ⚖️ AI Legal Rights Assistant
        </div>
        <div style="font-size: 1.2rem; font-weight: 400; opacity: 0.95; max-width: 800px; margin: 0 auto; line-height: 1.6;">
            Your intelligent guide to understanding legal rights, combining local knowledge with real-time information
        </div>
        <div style="margin-top: 1.5rem; padding: 1rem 2rem; background: rgba(255,255,255,0.15); border-radius: 10px; backdrop-filter: blur(10px); font-size: 1rem;">
            🚀 Enhanced with Web Search | 💾 Conversation History | 📤 Export Features
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer-box">
        <div style="display: flex; align-items: center; gap: 0.75rem; font-size: 1.2rem; font-weight: 700; color: #d84315; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem;">⚠️</span>
            <span>Important Legal Disclaimer</span>
        </div>
        <div style="color: #3e2723; line-height: 1.8; font-size: 1rem;">
            <p style="margin-bottom: 0.75rem;">
                <strong style="color: #bf360c;">Educational Purpose Only:</strong> 
                This platform provides general legal information. <strong style="color: #bf360c;">It is NOT a substitute for professional legal advice.</strong>
            </p>
            <p style="margin-top: 0.75rem; margin-bottom: 0.75rem;">
                <strong style="color: #bf360c;">Please Note:</strong> 
                Laws change frequently. The information may not be complete, current, or applicable to your specific situation.
            </p>
            <p style="margin-top: 0.75rem;">
                <strong style="color: #bf360c;">Action Required:</strong> 
                For specific legal matters, always consult with a qualified legal professional.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #667eea; margin-bottom: 0.5rem;">📚 Features</h2>
            <p style="color: #718096; font-size: 0.9rem;">Enhanced AI Assistant</p>
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
        top_k = st.slider(
            "Sources per answer", 
            1, 5, 3,
            help="More sources = more comprehensive answers"
        )
        
        use_web_search = st.checkbox(
            "🌐 Enable Web Search",
            value=False,
            help="Search the internet for additional information (requires internet)"
        )
        
        st.markdown("---")
        
        # Actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.session_state.messages:
                json_str = export_conversation()
                st.download_button(
                    "📥 Export",
                    json_str,
                    file_name=f"conversation_{st.session_state.conversation_id}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        st.markdown("---")
        
        # Info
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 1.5rem; border-left: 4px solid #667eea;">
            <div style="font-weight: 600; color: #2d3748; margin-bottom: 0.5rem; font-size: 1.1rem;">
                💡 Features
            </div>
            <div style="color: #4a5568; line-height: 1.6; font-size: 0.95rem;">
                • RAG-based retrieval<br>
                • Web search integration<br>
                • Source citations<br>
                • Conversation export<br>
                • Interactive chat
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize RAG
    if not st.session_state.rag_initialized:
        with st.status("🚀 Initializing AI System...", expanded=True) as status:
            st.write("Loading models and documents...")
            rag, error, count = load_rag_pipeline_safe()
            
            if error:
                status.update(label="❌ Initialization Failed", state="error")
                st.error(f"Error: {error}")
                st.stop()
            else:
                st.session_state.rag_pipeline = rag
                st.session_state.rag_initialized = True
                status.update(label=f"✅ Ready! {count} documents loaded", state="complete")
                time.sleep(1)
                st.rerun()
    
    # Chat Interface
    st.markdown('<div style="background: white; border-radius: 15px; padding: 2rem; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">', unsafe_allow_html=True)
    st.markdown("### 💬 Ask About Your Legal Rights")
    
    # Display chat history
    for msg in st.session_state.messages:
        display_message(
            msg['role'], 
            msg['content'], 
            msg.get('sources'),
            msg.get('web_sources')
        )
    
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
                        user_question = q
                        # Add user message
                        st.session_state.messages.append({
                            'role': 'user',
                            'content': user_question,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Get AI response
                        try:
                            result = st.session_state.rag_pipeline.query(
                                user_question, 
                                top_k=top_k,
                                use_web_search=use_web_search
                            )
                            
                            # Add assistant response
                            st.session_state.messages.append({
                                'role': 'assistant',
                                'content': result['answer'],
                                'sources': result.get('sources', []),
                                'web_sources': result.get('web_sources', []),
                                'timestamp': datetime.now().isoformat()
                            })
                            
                        except Exception as e:
                            st.session_state.messages.append({
                                'role': 'assistant',
                                'content': "I apologize, but I encountered an error. Please try again.",
                                'error': str(e),
                                'timestamp': datetime.now().isoformat()
                            })
                        
                        st.rerun()
    
    st.markdown("---")
    
    # Input Area
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_question = st.text_input(
            "Your question:",
            key="question_input",
            label_visibility="collapsed",
            placeholder="e.g., What are my rights as a worker?"
        )
    
    with col2:
        send_clicked = st.button("Send", type="primary", use_container_width=True)
    
    # Handle question submission
    if send_clicked and user_question:
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_question,
            'timestamp': datetime.now().isoformat()
        })
        
        # Get AI response
        try:
            with st.spinner("🤔 Analyzing documents and searching the web..."):
                result = st.session_state.rag_pipeline.query(
                    user_question, 
                    top_k=top_k,
                    use_web_search=use_web_search
                )
                
                # Add assistant response
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': result['answer'],
                    'sources': result.get('sources', []),
                    'web_sources': result.get('web_sources', []),
                    'timestamp': datetime.now().isoformat()
                })
                
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
            st.session_state.messages.append({
                'role': 'assistant',
                'content': "I apologize, but I encountered an error. Please try again.",
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; margin-top: 3rem; color: #718096; border-top: 2px solid #e2e8f0;">
        <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #4a5568;">
            AI Legal Rights Assistant
        </div>
        <div style="font-size: 0.9rem;">
            Empowering citizens through legal knowledge • Enhanced with AI & Web Search
        </div>
        <div style="margin-top: 1rem; font-size: 0.85rem; color: #a0aec0;">
            Built with ❤️ using Streamlit, HuggingFace, ChromaDB & AI
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

