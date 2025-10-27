"""
AI Legal Aid Chatbot - Gradio Interface
Alternative polished interface using Gradio
"""

import os
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['USE_TORCH'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import gradio as gr
from pathlib import Path
import traceback

# Global RAG pipeline
rag_pipeline = None


def initialize_rag():
    """Initialize RAG pipeline"""
    global rag_pipeline
    
    try:
        from rag_pipeline import RAGPipeline
        
        rag = RAGPipeline(
            data_dir="data",
            db_dir="db",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            llm_model="google/flan-t5-small"
        )
        
        # Ingest if needed
        doc_count = rag.collection.count()
        if doc_count == 0:
            print("📚 Processing PDFs...")
            num_chunks = rag.ingest_pdfs()
            print(f"✅ Processed {num_chunks} chunks")
        
        rag_pipeline = rag
        return f"✅ System ready! Knowledge base: {doc_count} text chunks"
        
    except Exception as e:
        return f"❌ Error: {str(e)}\n\n{traceback.format_exc()}"


def chat_response(message, history, num_sources):
    """Generate chat response"""
    global rag_pipeline
    
    if rag_pipeline is None:
        return "⚠️ System not initialized. Please wait..."
    
    try:
        result = rag_pipeline.query(message, top_k=num_sources)
        
        # Format response with sources
        response = f"**Answer:**\n{result['answer']}\n\n"
        response += "**📚 Sources:**\n"
        
        for i, source in enumerate(result['sources'], 1):
            response += f"\n{i}. **{source['source']}** (Page {source['page']})\n"
            response += f"   _{source['snippet']}_\n"
        
        return response
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_pdf_list():
    """Get list of PDFs"""
    data_dir = Path("data")
    if data_dir.exists():
        pdf_files = list(data_dir.glob("*.pdf"))
        return "\n".join([f"- {pdf.name}" for pdf in pdf_files])
    return "No PDFs found"


# Create Gradio interface
with gr.Blocks(
    title="AI Legal Aid Chatbot",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="purple"
    ),
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    .disclaimer {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    """
) as demo:
    
    # Header
    gr.Markdown("""
    # ⚖️ AI Legal Aid Chatbot
    ### Get information about Labour Laws, Consumer Rights & Digital Privacy
    """)
    
    # Disclaimer
    gr.Markdown("""
    <div class="disclaimer">
    <strong>⚠️ DISCLAIMER:</strong> This chatbot is for informational purposes only and does not constitute legal advice. 
    For specific legal matters, please consult a qualified legal professional or official authority.
    </div>
    """)
    
    with gr.Row():
        # Main chat area
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                height=500,
                label="Chat History",
                bubble_full_width=False
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask your legal question here...",
                    label="Your Question",
                    scale=4
                )
                send_btn = gr.Button("🚀 Send", scale=1, variant="primary")
            
            gr.Examples(
                examples=[
                    "What are the basic rights of workers in India?",
                    "How can I file a consumer complaint?",
                    "What is the minimum wage law?",
                    "What are my digital privacy rights?"
                ],
                inputs=msg,
                label="💡 Example Questions"
            )
        
        # Sidebar
        with gr.Column(scale=1):
            gr.Markdown("## ℹ️ About")
            gr.Markdown("""
            This chatbot uses **RAG** to provide information based on official documents.
            
            **Features:**
            - 🔒 Completely offline
            - 📄 Grounded in documents
            - 🎯 Cites sources
            - ⚡ Fast inference
            """)
            
            gr.Markdown("## 📖 Knowledge Base")
            pdf_list = gr.Textbox(
                value=get_pdf_list(),
                label="Loaded Documents",
                lines=5,
                interactive=False
            )
            
            gr.Markdown("## 🔧 Settings")
            num_sources = gr.Slider(
                minimum=1,
                maximum=5,
                value=3,
                step=1,
                label="Number of Sources"
            )
            
            status = gr.Textbox(
                label="System Status",
                value="Initializing...",
                interactive=False
            )
            
            init_btn = gr.Button("🔄 Restart System", variant="secondary")
    
    # Event handlers
    def respond(message, chat_history, num_sources):
        bot_message = chat_response(message, chat_history, num_sources)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    send_btn.click(
        respond,
        inputs=[msg, chatbot, num_sources],
        outputs=[msg, chatbot]
    )
    
    msg.submit(
        respond,
        inputs=[msg, chatbot, num_sources],
        outputs=[msg, chatbot]
    )
    
    init_btn.click(
        initialize_rag,
        outputs=status
    )
    
    # Initialize on load
    demo.load(
        initialize_rag,
        outputs=status
    )
    
    # Footer
    gr.Markdown("""
    ---
    <div style='text-align: center; color: #666;'>
    Built with ❤️ using Gradio, HuggingFace, ChromaDB & Sentence Transformers<br>
    🔒 100% Offline | 🎯 RAG-Powered | 📚 Source-Grounded
    </div>
    """)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
