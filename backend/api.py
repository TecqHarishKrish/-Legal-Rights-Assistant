"""
FastAPI Backend for Legal Rights Education Platform
Provides REST API for the chatbot
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['USE_TORCH'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
from datetime import datetime

# Import RAG pipeline
from rag_pipeline_enhanced import EnhancedRAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal Rights Education API",
    description="API for AI-powered legal rights education platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG pipeline instance
rag_pipeline: Optional[EnhancedRAGPipeline] = None


# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    top_k: int = 3
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are the basic rights of workers in India?",
                "top_k": 3
            }
        }


class Source(BaseModel):
    source: str
    page: int
    snippet: str


class AnswerResponse(BaseModel):
    answer: str
    sources: List[Source]
    timestamp: str
    processing_time: float


class HealthResponse(BaseModel):
    status: str
    message: str
    documents_loaded: int
    model_ready: bool


@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup"""
    global rag_pipeline
    
    logger.info("Initializing RAG Pipeline...")
    try:
        rag_pipeline = EnhancedRAGPipeline(
            data_dir="../data",
            db_dir="../db",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            llm_model="google/flan-t5-base"
        )
        
        # Check if documents are loaded
        doc_count = rag_pipeline.collection.count()
        if doc_count == 0:
            logger.info("No documents found. Ingesting PDFs...")
            doc_count = rag_pipeline.ingest_pdfs()
        
        logger.info(f"✅ RAG Pipeline ready with {doc_count} documents")
        
    except Exception as e:
        logger.error(f"Failed to initialize RAG pipeline: {str(e)}")
        rag_pipeline = None


@app.get("/", response_model=Dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Legal Rights Education API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "ask": "/api/ask",
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
            model_ready=False
        )
    
    doc_count = rag_pipeline.collection.count()
    
    return HealthResponse(
        status="healthy",
        message="System operational",
        documents_loaded=doc_count,
        model_ready=True
    )


@app.post("/api/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a legal question and get an AI-generated answer
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
            top_k=request.top_k
        )
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Format sources
        sources = [
            Source(
                source=s['source'],
                page=s['page'],
                snippet=s['snippet']
            )
            for s in result.get('sources', [])
        ]
        
        return AnswerResponse(
            answer=result['answer'],
            sources=sources,
            timestamp=datetime.now().isoformat(),
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.get("/api/documents")
async def list_documents():
    """List all loaded documents"""
    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
    
    data_dir = Path("../data")
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
