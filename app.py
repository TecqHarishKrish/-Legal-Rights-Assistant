"""
Streamlit UI for AI Legal Aid Chatbot
"""

import os
# Disable TensorFlow (we use PyTorch only)
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['USE_TORCH'] = '1'

import streamlit as st
import time
from pathlib import Path
import logging

from rag_pipeline import RAGPipeline
from prompts import DISCLAIMER_TEXT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Legal Aid Chatbot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .disclaimer-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .answer-box {
        background-color: #e8f4f8;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .source-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .key-points {
        background-color: #e7f3e7;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #155a8a;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_rag_pipeline():
    """
    Load and cache the RAG pipeline
    """
    with st.spinner("🔄 Initializing AI Legal Aid System..."):
        rag = RAGPipeline(
            data_dir="data",
            db_dir="db",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            llm_model="google/flan-t5-small"
        )
        return rag


def parse_answer(raw_answer: str) -> dict:
    """
    Parse the generated answer into structured format
    
    Args:
        raw_answer: Raw answer from LLM
        
    Returns:
        Dict with answer, key_points
    """
    result = {
        "answer": "",
        "key_points": []
    }
    
    lines = raw_answer.strip().split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for section headers
        if line.lower().startswith('answer:'):
            current_section = 'answer'
            answer_text = line[7:].strip()
            if answer_text:
                result['answer'] = answer_text
        elif line.lower().startswith('key points:'):
            current_section = 'key_points'
        elif line.startswith('-') or line.startswith('•'):
            if current_section == 'key_points':
                point = line.lstrip('-•').strip()
                if point:
                    result['key_points'].append(point)
        else:
            # Continue previous section
            if current_section == 'answer':
                result['answer'] += ' ' + line
            elif current_section == 'key_points' and line:
                # Sometimes key points don't have bullets
                result['key_points'].append(line)
    
    # If no structured answer found, use the whole text
    if not result['answer']:
        result['answer'] = raw_answer
    
    return result


def display_sources(sources: list):
    """
    Display source citations
    
    Args:
        sources: List of source dicts
    """
    st.markdown("### 📚 Sources")
    
    for i, source in enumerate(sources, 1):
        with st.expander(f"📄 {source['source']} - Page {source['page']}"):
            st.markdown(f"**Snippet:**")
            st.text(source['snippet'])


def main():
    """
    Main Streamlit application
    """
    
    # Header
    st.markdown('<div class="main-header">⚖️ AI Legal Aid Chatbot</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Get information about Labour Laws, Consumer Rights & Digital Privacy</div>',
        unsafe_allow_html=True
    )
    
    # Disclaimer
    st.markdown(f'<div class="disclaimer-box">{DISCLAIMER_TEXT}</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ℹ️ About")
        st.markdown("""
        This chatbot uses **Retrieval-Augmented Generation (RAG)** to provide 
        information about legal rights based on official documents.
        
        **Features:**
        - 🔒 Completely offline
        - 📄 Grounded in official documents
        - 🎯 Cites sources for transparency
        - ⚡ Fast local inference
        """)
        
        st.markdown("---")
        st.markdown("## 📖 Knowledge Base")
        
        data_dir = Path("data")
        if data_dir.exists():
            pdf_files = list(data_dir.glob("*.pdf"))
            if pdf_files:
                st.markdown(f"**{len(pdf_files)} documents loaded:**")
                for pdf in pdf_files:
                    st.markdown(f"- {pdf.name}")
            else:
                st.warning("No PDF files found in data directory")
        
        st.markdown("---")
        st.markdown("## 🔧 Settings")
        
        top_k = st.slider(
            "Number of sources to retrieve",
            min_value=1,
            max_value=5,
            value=3,
            help="More sources = more context but slower response"
        )
        
        force_reingest = st.checkbox(
            "Force re-ingest PDFs",
            value=False,
            help="Re-process all PDFs (use if you added new documents)"
        )
        
        if st.button("🔄 Re-initialize System"):
            st.cache_resource.clear()
            st.success("System cache cleared! Reload the page.")
    
    # Initialize RAG pipeline
    try:
        rag = load_rag_pipeline()
        
        # Check if documents are ingested
        doc_count = rag.collection.count()
        
        if doc_count == 0 or force_reingest:
            with st.spinner("📚 Ingesting PDF documents... This may take a few minutes."):
                num_chunks = rag.ingest_pdfs(force_reingest=force_reingest)
                st.success(f"✅ Successfully ingested {num_chunks} text chunks!")
        else:
            st.info(f"📊 Knowledge base loaded: {doc_count} text chunks available")
        
    except Exception as e:
        st.error(f"❌ Error initializing system: {e}")
        logger.error(f"Initialization error: {e}", exc_info=True)
        st.stop()
    
    # Main query interface
    st.markdown("---")
    st.markdown("## 💬 Ask Your Question")
    
    # Example questions
    with st.expander("💡 Example Questions"):
        st.markdown("""
        - What are the basic rights of workers in India?
        - What is the minimum wage law?
        - How can I file a consumer complaint?
        - What are my rights regarding digital privacy?
        - What is the working hours limit for employees?
        - How do I get compensation for defective products?
        """)
    
    # Query input
    query = st.text_area(
        "Enter your question:",
        height=100,
        placeholder="e.g., What are the basic rights of workers in India?"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        submit_button = st.button("🔍 Get Answer", type="primary")
    with col2:
        clear_button = st.button("🗑️ Clear")
    
    if clear_button:
        st.rerun()
    
    # Process query
    if submit_button and query.strip():
        with st.spinner("🤔 Thinking... Retrieving relevant information and generating answer..."):
            start_time = time.time()
            
            try:
                # Get answer from RAG pipeline
                result = rag.query(query, top_k=top_k)
                
                elapsed_time = time.time() - start_time
                
                # Parse answer
                parsed = parse_answer(result['raw_answer'])
                
                # Display results
                st.markdown("---")
                st.markdown("## 📝 Response")
                
                # Answer section
                st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                st.markdown("### 💡 Answer")
                st.markdown(parsed['answer'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Key points section
                if parsed['key_points']:
                    st.markdown('<div class="key-points">', unsafe_allow_html=True)
                    st.markdown("### 🔑 Key Points")
                    for point in parsed['key_points']:
                        st.markdown(f"- {point}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Sources section
                if result['sources']:
                    display_sources(result['sources'])
                
                # Performance metrics
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("⏱️ Response Time", f"{elapsed_time:.2f}s")
                with col2:
                    st.metric("📄 Sources Used", len(result['sources']))
                
            except Exception as e:
                st.error(f"❌ Error processing query: {e}")
                logger.error(f"Query error: {e}", exc_info=True)
    
    elif submit_button:
        st.warning("⚠️ Please enter a question first!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>Built with ❤️ using Streamlit, LangChain, HuggingFace & ChromaDB</p>
        <p>🔒 100% Offline | 🎯 RAG-Powered | 📚 Source-Grounded</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
