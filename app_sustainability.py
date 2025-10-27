"""
Streamlit App for AI Sustainability Advisor
"""

import streamlit as st
import os
from pathlib import Path
from rag_pipeline_sustainability import SustainabilityRAGPipeline
from prompts_sustainability import RAG_PROMPT_TEMPLATE, QUERY_EXAMPLES, DISCLAIMER

# Page config
st.set_page_config(
    page_title="AI Sustainability Advisor",
    page_icon="♻️",
    layout="wide"
)

# Title and description
st.title("🌍 AI Sustainability Advisor")
st.markdown("Get recycling and waste management advice using local guidelines")

# Initialize session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'data_ingested' not in st.session_state:
    st.session_state.data_ingested = False

# Sidebar for setup
with st.sidebar:
    st.header("⚙️ Setup")
    
    # Check if data directory exists
    data_dir = Path("data_sustainability")
    pdf_files = list(data_dir.glob("*.pdf")) if data_dir.exists() else []
    
    if not pdf_files:
        st.warning("📁 No PDF files found in `data_sustainability/` directory.")
        st.info("""
        **To get started:**
        1. Create `data_sustainability/` folder
        2. Add PDF waste management guidelines
        3. Click 'Initialize System' button
        """)
    else:
        st.success(f"📁 Found {len(pdf_files)} PDF file(s):")
        for pdf in pdf_files:
            st.text(f"  • {pdf.name}")
    
    # Initialize button
    if st.button("🚀 Initialize System", type="primary", disabled=not pdf_files):
        with st.spinner("Initializing RAG pipeline..."):
            try:
                pipeline = SustainabilityRAGPipeline()
                st.session_state.rag_pipeline = pipeline
                
                # Ingest PDFs
                with st.spinner("Ingesting PDF documents..."):
                    result = pipeline.ingest_pdfs(str(data_dir))
                    
                    if result["status"] == "success":
                        st.session_state.data_ingested = True
                        st.success(f"✅ Ingested {result['total_chunks']} chunks from {result['documents_processed']} documents")
                    else:
                        st.error(f"Error: {result.get('message', 'Unknown error')}")
                
            except Exception as e:
                st.error(f"Initialization error: {e}")
    
    if st.session_state.data_ingested:
        st.success("✅ System Ready!")

# Main content area
if not st.session_state.data_ingested:
    st.info("👈 Please initialize the system in the sidebar first.")
    
    # Display example queries
    st.subheader("📋 Example Queries")
    st.markdown("Once initialized, you can ask questions like:")
    for example in QUERY_EXAMPLES:
        st.markdown(f"- {example}")
    
else:
    # Chat interface
    st.subheader("💬 Ask a Question")
    
    # Display example queries as clickable chips
    st.markdown("**Try these examples:**")
    cols = st.columns(3)
    for idx, example in enumerate(QUERY_EXAMPLES[:3]):
        if cols[idx].button(example, key=f"example_{idx}"):
            st.session_state.example_query = example
    
    # Query input
    default_query = st.session_state.get('example_query', '')
    user_query = st.text_input(
        "Enter your question about waste management and recycling:",
        value=default_query,
        key="user_query_input"
    )
    
    if st.button("🔍 Ask", type="primary") or default_query:
        if user_query:
            with st.spinner("🔍 Searching knowledge base..."):
                try:
                    # Query RAG pipeline
                    result = st.session_state.rag_pipeline.query(
                        user_query,
                        RAG_PROMPT_TEMPLATE,
                        k=3
                    )
                    
                    # Display answer
                    st.subheader("💡 Answer")
                    st.write(result['answer'])
                    
                    # Display key points if available
                    if result.get('key_points'):
                        st.subheader("🔑 Key Points")
                        for point in result['key_points']:
                            st.markdown(f"- {point}")
                    
                    # Display sources
                    if result.get('sources'):
                        st.subheader("📚 Sources")
                        for i, source in enumerate(result['sources'], 1):
                            with st.expander(f"Source {i}: {source['document']} (Page {source['page']})"):
                                st.text(source['snippet'])
                    
                except Exception as e:
                    st.error(f"Error processing query: {e}")
        else:
            st.warning("Please enter a question")
    
    # Clear example query from session state
    if 'example_query' in st.session_state:
        del st.session_state.example_query

# Disclaimer at bottom
st.markdown("---")
st.markdown(DISCLAIMER)

# Footer
st.markdown("---")
st.markdown("### 🛠️ Technical Details")
st.caption("""
- **Embeddings Model:** sentence-transformers/all-MiniLM-L6-v2
- **Generation Model:** google/flan-t5-small
- **Vector Store:** ChromaDB (local)
- **Framework:** LangChain + Streamlit
""")

