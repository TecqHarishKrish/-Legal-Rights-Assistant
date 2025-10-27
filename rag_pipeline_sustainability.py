"""
RAG Pipeline for AI Sustainability Advisor
Handles PDF ingestion, embeddings, retrieval, and generation
"""

import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import uuid
from typing import List, Dict, Any, Tuple
from pathlib import Path

class SustainabilityRAGPipeline:
    """Main RAG pipeline for sustainability advisor"""
    
    def __init__(self, db_path: str = "./db_sustainability", model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize RAG pipeline
        
        Args:
            db_path: Path to ChromaDB directory
            model_name: HuggingFace model for embeddings
        """
        # Initialize embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer(model_name)
        
        # Initialize ChromaDB
        print("Initializing ChromaDB...")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="sustainability_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize LLM pipeline
        print("Loading generation model...")
        self.llm = pipeline(
            "text2text-generation",
            model="google/flan-t5-small",
            device=-1  # CPU
        )
        
        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )
        
    def ingest_pdfs(self, pdf_directory: str) -> Dict[str, Any]:
        """
        Ingest PDF documents from directory
        
        Args:
            pdf_directory: Path to directory containing PDFs
            
        Returns:
            Dictionary with ingestion statistics
        """
        pdf_files = list(Path(pdf_directory).glob("*.pdf"))
        
        if not pdf_files:
            return {"status": "error", "message": "No PDF files found"}
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        for pdf_path in pdf_files:
            print(f"Processing {pdf_path.name}...")
            try:
                # Load PDF
                loader = PyPDFLoader(str(pdf_path))
                documents = loader.load()
                
                # Split into chunks
                chunks = self.text_splitter.split_documents(documents)
                
                # Prepare data for ChromaDB
                for i, chunk in enumerate(chunks):
                    chunk_id = str(uuid.uuid4())
                    all_chunks.append(chunk.page_content)
                    all_metadatas.append({
                        "document": pdf_path.name,
                        "page": chunk.metadata.get("page", 0),
                        "chunk_index": i
                    })
                    all_ids.append(chunk_id)
                    
            except Exception as e:
                print(f"Error processing {pdf_path.name}: {e}")
                continue
        
        # Add to ChromaDB
        if all_chunks:
            # Generate embeddings
            print("Generating embeddings...")
            embeddings = self.embedding_model.encode(all_chunks).tolist()
            
            # Add to collection
            print("Storing in ChromaDB...")
            self.collection.add(
                ids=all_ids,
                embeddings=embeddings,
                documents=all_chunks,
                metadatas=all_metadatas
            )
            
            return {
                "status": "success",
                "documents_processed": len(pdf_files),
                "total_chunks": len(all_chunks)
            }
        
        return {"status": "error", "message": "No chunks created"}
    
    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from ChromaDB
        
        Args:
            query: User query
            k: Number of results to retrieve
            
        Returns:
            List of relevant documents with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )
            
            # Format results
            retrieved_docs = []
            if results.get('documents') and len(results['documents'][0]) > 0:
                for i in range(len(results['documents'][0])):
                    retrieved_docs.append({
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i] if results.get('metadatas') else {},
                        "distance": results['distances'][0][i] if results.get('distances') else None
                    })
            
            return retrieved_docs
        except Exception as e:
            print(f"Retrieval error: {e}")
            return []
    
    def generate_answer(self, query: str, context: str, prompt_template: str) -> str:
        """
        Generate answer using RAG
        
        Args:
            query: User query
            context: Retrieved context from ChromaDB
            prompt_template: Template for prompt construction
            
        Returns:
            Generated answer
        """
        # Construct prompt
        prompt = prompt_template.format(query=query, context=context)
        
        # Generate with LLM
        try:
            result = self.llm(
                prompt,
                max_length=512,
                min_length=50,
                do_sample=False,
                num_beams=3
            )
            
            return result[0]['generated_text']
        except Exception as e:
            print(f"Generation error: {e}")
            return "I'm having trouble processing your query. Please rephrase it."
    
    def query(self, user_query: str, prompt_template: str, k: int = 3) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve + generate
        
        Args:
            user_query: User's question
            prompt_template: Prompt template string
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer, key_points, and sources
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(user_query, k=k)
        
        if not retrieved_docs:
            return {
                "answer": "I don't know. Please consult your local waste management authority.",
                "key_points": [],
                "sources": []
            }
        
        # Combine context
        context = "\n\n".join([doc['content'] for doc in retrieved_docs])
        
        # Generate answer
        generated_text = self.generate_answer(user_query, context, prompt_template)
        
        # Parse response (simple extraction)
        answer = generated_text
        key_points = self._extract_key_points(generated_text)
        sources = [{
            "document": doc['metadata']['document'],
            "page": doc['metadata']['page'],
            "snippet": doc['content'][:200] + "..."
        } for doc in retrieved_docs]
        
        return {
            "answer": answer,
            "key_points": key_points,
            "sources": sources
        }
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from generated text"""
        lines = text.split('\n')
        key_points = []
        for line in lines:
            if line.strip().startswith('-') or line.strip().startswith('•'):
                key_points.append(line.strip())
        
        return key_points if key_points else [text[:100] + "..."]  # Fallback
    
    def is_ready(self) -> bool:
        """Check if the pipeline is ready"""
        try:
            return self.collection.count() > 0
        except:
            return False

