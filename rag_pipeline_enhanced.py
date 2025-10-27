"""
Enhanced RAG Pipeline for AI Legal Aid Chatbot
Improved retrieval, generation, and error handling
"""

import os
import logging
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import re

# Disable TensorFlow (we use PyTorch only)
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['USE_TORCH'] = '1'

# PDF processing
from pypdf import PdfReader

# Embeddings and vector store
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# LLM for generation
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

# Prompts
from prompts import RAG_PROMPT_TEMPLATE, SYSTEM_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedRAGPipeline:
    """
    Enhanced RAG pipeline with better retrieval and generation
    """
    
    def __init__(
        self,
        data_dir: str = "data",
        db_dir: str = "db",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "google/flan-t5-base",
        chunk_size: int = 600,
        chunk_overlap: int = 100,
        collection_name: str = "legal_docs"
    ):
        """
        Initialize Enhanced RAG pipeline
        """
        self.data_dir = Path(data_dir)
        self.db_dir = Path(db_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.collection_name = collection_name
        
        logger.info("Initializing Enhanced RAG Pipeline...")
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize ChromaDB
        logger.info(f"Initializing ChromaDB at {self.db_dir}")
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path=str(self.db_dir))
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection(name=self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Legal documents for RAG"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
        
        # Initialize LLM with better configuration
        logger.info(f"Loading LLM: {llm_model}")
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model)
        self.llm = AutoModelForSeq2SeqLM.from_pretrained(
            llm_model,
            torch_dtype=torch.float32
        )
        
        # Set device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.llm.to(self.device)
        logger.info(f"Using device: {self.device}")
        
        logger.info("RAG Pipeline initialized successfully!")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,;:!?()\-\'\"]+', '', text)
        return text.strip()
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Split text into overlapping chunks with metadata
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if len(chunk_text.strip()) > 50:  # Minimum chunk size
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        **metadata,
                        'chunk_index': len(chunks),
                        'word_count': len(chunk_words)
                    }
                })
        
        return chunks
    
    def ingest_pdfs(self) -> int:
        """
        Ingest all PDFs from data directory
        """
        if not self.data_dir.exists():
            logger.error(f"Data directory not found: {self.data_dir}")
            return 0
        
        pdf_files = list(self.data_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.data_dir}")
            return 0
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        all_chunks = []
        all_embeddings = []
        all_ids = []
        all_metadatas = []
        
        for pdf_path in pdf_files:
            logger.info(f"Processing: {pdf_path.name}")
            
            try:
                reader = PdfReader(str(pdf_path))
                
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    
                    if text.strip():
                        cleaned_text = self.clean_text(text)
                        
                        # Create chunks
                        chunks = self.chunk_text(
                            cleaned_text,
                            {
                                'source': pdf_path.name,
                                'page': page_num + 1,
                                'total_pages': len(reader.pages)
                            }
                        )
                        
                        for chunk in chunks:
                            chunk_id = f"{pdf_path.stem}_p{page_num+1}_c{chunk['metadata']['chunk_index']}"
                            
                            all_chunks.append(chunk['text'])
                            all_ids.append(chunk_id)
                            all_metadatas.append(chunk['metadata'])
                
                logger.info(f"✓ Processed {pdf_path.name}: {len(reader.pages)} pages")
                
            except Exception as e:
                logger.error(f"Error processing {pdf_path.name}: {str(e)}")
                continue
        
        if not all_chunks:
            logger.error("No text chunks extracted from PDFs")
            return 0
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(all_chunks)} chunks...")
        all_embeddings = self.embedding_model.encode(
            all_chunks,
            show_progress_bar=True,
            convert_to_numpy=True
        ).tolist()
        
        # Add to ChromaDB
        logger.info("Adding to vector database...")
        self.collection.add(
            ids=all_ids,
            embeddings=all_embeddings,
            documents=all_chunks,
            metadatas=all_metadatas
        )
        
        logger.info(f"✅ Successfully ingested {len(all_chunks)} text chunks!")
        return len(all_chunks)
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve relevant documents for a query
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        retrieved_docs = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                retrieved_docs.append({
                    'text': results['documents'][0][i],
                    'source': results['metadatas'][0][i].get('source', 'Unknown'),
                    'page': results['metadatas'][0][i].get('page', 'N/A'),
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return retrieved_docs
    
    def generate_answer(self, query: str, context_docs: List[Dict]) -> str:
        """
        Generate answer using LLM with improved prompting
        """
        # Prepare context
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            context_parts.append(
                f"[Source {i}: {doc['source']}, Page {doc['page']}]\n{doc['text']}"
            )
        
        context = "\n\n".join(context_parts)
        
        # Create prompt
        prompt = RAG_PROMPT_TEMPLATE.format(
            context=context,
            question=query
        )
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            max_length=1024,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate with better parameters
        with torch.no_grad():
            outputs = self.llm.generate(
                **inputs,
                max_length=512,
                min_length=100,
                num_beams=4,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.2,
                length_penalty=1.0,
                early_stopping=True
            )
        
        # Decode
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return answer
    
    def query(self, question: str, top_k: int = 3) -> Dict:
        """
        Complete RAG query: retrieve + generate
        """
        try:
            # Retrieve relevant documents
            logger.info(f"Retrieving top {top_k} documents for: {question}")
            retrieved_docs = self.retrieve(question, top_k=top_k)
            
            if not retrieved_docs:
                return {
                    'answer': "I don't have enough information to answer this question. Please try rephrasing or ask about topics covered in the legal documents.",
                    'sources': []
                }
            
            # Generate answer
            logger.info("Generating answer...")
            answer = self.generate_answer(question, retrieved_docs)
            
            # Format sources
            sources = [
                {
                    'source': doc['source'],
                    'page': doc['page'],
                    'snippet': doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text']
                }
                for doc in retrieved_docs
            ]
            
            return {
                'answer': answer,
                'sources': sources
            }
            
        except Exception as e:
            logger.error(f"Error in query: {str(e)}")
            return {
                'answer': f"I encountered an error while processing your question: {str(e)}. Please try again.",
                'sources': []
            }


# Alias for backward compatibility
RAGPipeline = EnhancedRAGPipeline
