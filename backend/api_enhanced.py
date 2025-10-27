"""
Enhanced FastAPI Backend for Legal Rights Education Platform
Includes web search, conversation history, and enhanced features
"""

import os
import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['USE_TORCH'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
from datetime import datetime
from typing import List

# Import RAG pipeline
from rag_pipeline_advanced import AdvancedRAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal Rights Education API - Enhanced",
    description="Advanced API for AI-powered legal rights education platform with web search",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG pipeline instance
rag_pipeline: Optional[AdvancedRAGPipeline] = None

# In-memory conversation storage (for demo; use database in production)
conversations: Dict[str, List[Dict]] = {}


# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3
    use_web_search: bool = False
    conversation_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are the basic rights of workers in India?",
                "top_k": 3,
                "use_web_search": True
            }
        }


class Source(BaseModel):
    source: str
    page: str
    snippet: str


class AnswerResponse(BaseModel):
    answer: str
    sources: List[Source]
    web_sources: List[Source]
    conversation_id: str
    timestamp: str
    processing_time: float
    used_web_search: bool = False


class HealthResponse(BaseModel):
    status: str
    message: str
    documents_loaded: int
    model_ready: bool
    web_search_enabled: bool


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    messages: List[Dict]
    created_at: str
    updated_at: str


@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup"""
    global rag_pipeline
    
    logger.info("Initializing Advanced RAG Pipeline...")
    try:
        rag_pipeline = AdvancedRAGPipeline(
            data_dir="data",
            db_dir="db",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            llm_model="google/flan-t5-base",
            enable_web_search=True
        )
        
        # Check if documents are loaded
        doc_count = rag_pipeline.collection.count()
        if doc_count == 0:
            logger.info("No documents found. Ingesting PDFs...")
            doc_count = rag_pipeline.ingest_pdfs()
        
        logger.info(f"✅ Advanced RAG Pipeline ready with {doc_count} documents")
        logger.info(f"Web search: {'Enabled' if rag_pipeline.enable_web_search else 'Disabled'}")
        
    except Exception as e:
        logger.error(f"Failed to initialize RAG pipeline: {str(e)}")
        raise


@app.get("/", response_model=Dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Legal Rights Education API - Enhanced",
        "version": "2.0.0",
        "features": [
            "RAG-based document retrieval",
            "Web search integration",
            "Conversation history",
            "Source citations"
        ],
        "endpoints": {
            "health": "/health",
            "ask": "/api/ask",
            "conversations": "/api/conversations",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if rag_pipeline is None:
        return HealthResponse(
            status="error",
            message="RAG pipeline not initialized",
            documents_loaded=0,
            model_ready=False,
            web_search_enabled=False
        )
    
    doc_count = rag_pipeline.collection.count()
    
    return HealthResponse(
        status="healthy",
        message="System operational",
        documents_loaded=doc_count,
        model_ready=True,
        web_search_enabled=rag_pipeline.enable_web_search
    )


@app.post("/api/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a legal question and get an AI-generated answer with optional web search
    """
    if rag_pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="RAG pipeline not initialized. Please try again later."
        )
    
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    try:
        start_time = datetime.now()
        
        # Query the RAG pipeline
        result = rag_pipeline.query(
            question=request.question,
            top_k=request.top_k,
            use_web_search=request.use_web_search
        )
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Manage conversation
        conversation_id = request.conversation_id or f"conv_{datetime.now().timestamp()}"
        
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Add messages to conversation
        conversations[conversation_id].append({
            'role': 'user',
            'content': request.question,
            'timestamp': datetime.now().isoformat()
        })
        
        conversations[conversation_id].append({
            'role': 'assistant',
            'content': result['answer'],
            'sources': result.get('sources', []),
            'timestamp': datetime.now().isoformat()
        })
        
        # Format sources
        sources = [
            Source(
                source=s.get('source', 'Unknown'),
                page=str(s.get('page', 'N/A')),
                snippet=s.get('snippet', '')
            )
            for s in result.get('sources', [])
        ]
        
        web_sources = [
            Source(
                source=s.get('source', 'Unknown'),
                page='Web',
                snippet=s.get('snippet', '')
            )
            for s in result.get('web_sources', [])
        ]
        
        return AnswerResponse(
            answer=result['answer'],
            sources=sources,
            web_sources=web_sources,
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat(),
            processing_time=processing_time,
            used_web_search=result.get('used_web_search', False)
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversations:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    
    return ConversationHistoryResponse(
        conversation_id=conversation_id,
        messages=conversations[conversation_id],
        created_at=conversations[conversation_id][0]['timestamp'] if conversations[conversation_id] else datetime.now().isoformat(),
        updated_at=conversations[conversation_id][-1]['timestamp'] if conversations[conversation_id] else datetime.now().isoformat()
    )


@app.get("/api/conversations")
async def list_conversations():
    """List all conversations"""
    return {
        "conversations": [
            {
                "id": conv_id,
                "message_count": len(messages),
                "last_message": messages[-1]['timestamp'] if messages else None
            }
            for conv_id, messages in conversations.items()
        ],
        "total": len(conversations)
    }


@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id not in conversations:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    
    del conversations[conversation_id]
    return {"message": "Conversation deleted"}


@app.get("/api/documents")
async def list_documents():
    """List all loaded documents"""
    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
    
    data_dir = Path("data")
    if not data_dir.exists():
        return {"documents": []}
    
    pdf_files = list(data_dir.glob("*.pdf"))
    
    return {
        "documents": [
            {
                "name": pdf.name,
                "size": pdf.stat().st_size,
                "modified": datetime.fromtimestamp(pdf.stat().st_mtime).isoformat()
            }
            for pdf in pdf_files
        ],
        "total": len(pdf_files)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

