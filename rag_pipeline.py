"""
RAG Pipeline for AI Legal Aid Chatbot
Handles PDF ingestion, embeddings, retrieval, and generation
"""

import os
import logging
from typing import List, Dict, Tuple
from pathlib import Path

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
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Prompts
from prompts import RAG_PROMPT_TEMPLATE, SYSTEM_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Complete RAG pipeline for legal aid chatbot
    """
    
    def __init__(
        self,
        data_dir: str = "data",
        db_dir: str = "db",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "google/flan-t5-small",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        collection_name: str = "legal_docs"
    ):
        """
        Initialize RAG pipeline
        
        Args:
            data_dir: Directory containing PDF files
            db_dir: Directory for ChromaDB persistence
            embedding_model: HuggingFace embedding model name
            llm_model: HuggingFace LLM model name
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            collection_name: ChromaDB collection name
        """
        self.data_dir = Path(data_dir)
        self.db_dir = Path(db_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.collection_name = collection_name
        
        logger.info("Initializing RAG Pipeline...")
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize ChromaDB
        logger.info(f"Initializing ChromaDB at {self.db_dir}")
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.db_dir)
        )
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection(
                name=self.collection_name
            )
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Legal documents for RAG"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
        
        # Initialize LLM
        logger.info(f"Loading LLM: {llm_model}")
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model)
        self.llm = AutoModelForSeq2SeqLM.from_pretrained(llm_model)
        
        # Set device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.llm.to(self.device)
        logger.info(f"Using device: {self.device}")
        
        logger.info("RAG Pipeline initialized successfully!")
    
    def extract_text_from_pdf(self, pdf_path: Path) -> List[Dict[str, str]]:
        """
        Extract text from PDF file page by page
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of dicts with page text and metadata
        """
        logger.info(f"Extracting text from: {pdf_path.name}")
        pages = []
        
        try:
            reader = PdfReader(str(pdf_path))
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text.strip():  # Only add non-empty pages
                    pages.append({
                        "text": text,
                        "page_num": page_num,
                        "source": pdf_path.name
                    })
            logger.info(f"Extracted {len(pages)} pages from {pdf_path.name}")
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path.name}: {e}")
        
        return pages
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk_text.rfind('.')
                last_newline = chunk_text.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > self.chunk_size * 0.5:  # At least 50% of chunk
                    chunk_text = chunk_text[:break_point + 1]
                    end = start + break_point + 1
            
            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text.strip(),
                    "metadata": metadata.copy()
                })
            
            start = end - self.chunk_overlap
        
        return chunks
    
    def ingest_pdfs(self, force_reingest: bool = False) -> int:
        """
        Ingest all PDFs from data directory
        
        Args:
            force_reingest: If True, clear existing collection and reingest
            
        Returns:
            Number of chunks ingested
        """
        # Check if collection already has documents
        existing_count = self.collection.count()
        if existing_count > 0 and not force_reingest:
            logger.info(f"Collection already contains {existing_count} documents. Skipping ingestion.")
            logger.info("Use force_reingest=True to reingest.")
            return existing_count
        
        if force_reingest and existing_count > 0:
            logger.info("Force reingest: Deleting existing collection...")
            self.chroma_client.delete_collection(self.collection_name)
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Legal documents for RAG"}
            )
        
        logger.info(f"Starting PDF ingestion from {self.data_dir}")
        
        # Get all PDF files
        pdf_files = list(self.data_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {self.data_dir}")
            return 0
        
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        all_chunks = []
        
        # Process each PDF
        for pdf_path in pdf_files:
            pages = self.extract_text_from_pdf(pdf_path)
            
            for page_data in pages:
                metadata = {
                    "source": page_data["source"],
                    "page": page_data["page_num"]
                }
                chunks = self.chunk_text(page_data["text"], metadata)
                all_chunks.extend(chunks)
        
        if not all_chunks:
            logger.warning("No chunks created from PDFs")
            return 0
        
        logger.info(f"Created {len(all_chunks)} chunks. Computing embeddings...")
        
        # Prepare data for ChromaDB
        documents = [chunk["text"] for chunk in all_chunks]
        metadatas = [chunk["metadata"] for chunk in all_chunks]
        ids = [f"chunk_{i}" for i in range(len(all_chunks))]
        
        # Compute embeddings
        embeddings = self.embedding_model.encode(
            documents,
            show_progress_bar=True,
            convert_to_numpy=True
        ).tolist()
        
        # Add to ChromaDB
        logger.info("Adding chunks to ChromaDB...")
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Successfully ingested {len(all_chunks)} chunks!")
        return len(all_chunks)
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve top-k relevant chunks for query
        
        Args:
            query: User query
            top_k: Number of chunks to retrieve
            
        Returns:
            List of retrieved chunks with metadata
        """
        logger.info(f"Retrieving top-{top_k} chunks for query: {query[:50]}...")
        
        # Encode query
        query_embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True
        ).tolist()
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        retrieved_chunks = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                retrieved_chunks.append({
                    "text": doc,
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks")
        return retrieved_chunks
    
    def generate_answer(self, query: str, context_chunks: List[Dict]) -> str:
        """
        Generate answer using LLM based on retrieved context
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            
        Returns:
            Generated answer
        """
        logger.info("Generating answer...")
        
        # Build context string with relevant content
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            source = chunk['metadata'].get('source', 'Unknown')
            page = chunk['metadata'].get('page', 'Unknown')
            text = chunk['text']
            
            # Only include context chunks that are actually relevant to the query
            if any(term.lower() in text.lower() for term in query.split()):
                context_parts.append(f"[Source {i}: {source} - Page {page}]\n{text}")
            
            # Limit to top 3 most relevant chunks to avoid overwhelming the model
            if len(context_parts) >= 3:
                break
        
        if not context_parts:
            return "I couldn't find specific information about that topic in the available documents. Please try rephrasing your question or ask about a different legal topic."
        
        context = "\n\n".join(context_parts)
        
        # Build prompt with clear instructions
        prompt = (
            "You are a legal assistant. Answer the question based on the provided context.\n"
            "If the context doesn't contain the answer, say 'The document doesn't provide specific information about this.'\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n"
            "Answer in a clear, concise manner. If listing items, use bullet points. "
            "If providing steps, number them. Keep your response focused and relevant to the question."
        )
        
        # Tokenize with appropriate length
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=1024,
            truncation=True,
            padding=True
        ).to(self.device)
        
        # Generate with conservative parameters to avoid repetition
        with torch.no_grad():
            outputs = self.llm.generate(
                **inputs,
                max_new_tokens=300,  # Limit response length
                min_length=30,       # Ensure reasonable minimum length
                num_beams=3,         # Balance between quality and speed
                early_stopping=True,  # Stop when the model is done
                temperature=0.7,     # Slightly random but focused
                do_sample=True,      # Enable sampling for better quality
                top_k=50,            # Limit to top-k most likely next tokens
                top_p=0.9,           # Nucleus sampling for better quality
                repetition_penalty=1.2,  # Discourage repetition
                no_repeat_ngram_size=3,  # Avoid repeating n-grams
                length_penalty=1.0    # Neutral length penalty
            )
        
        # Decode and clean up the response
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Post-process the answer to remove any repetition
        answer = self._post_process_answer(answer, query)
        
        logger.info(f"Generated answer (length: {len(answer)} chars)")
        return answer
    
    def _post_process_answer(self, answer: str, query: str) -> str:
        """Clean up the generated answer to ensure quality."""
        # Remove any repeated sentences
        sentences = [s.strip() for s in answer.split('.') if s.strip()]
        unique_sentences = []
        seen = set()
        
        for sent in sentences:
            # Simple deduplication of similar sentences
            words = sent.lower().split()
            key = ' '.join(sorted(set(words))[:5])  # Create a simple fingerprint
            
            if key not in seen and len(sent) > 10:  # Only keep meaningful sentences
                seen.add(key)
                unique_sentences.append(sent)
        
        # Reconstruct the answer
        cleaned = '. '.join(unique_sentences) + ('.' if unique_sentences else '')
        
        # Ensure the answer is relevant to the query
        query_terms = set(term.lower() for term in query.split() if len(term) > 3)
        answer_terms = set(cleaned.lower().split())
        
        # If answer doesn't seem relevant to the query, be honest about it
        if not any(term in answer_terms for term in query_terms):
            return "I couldn't find specific information about that topic in the available documents. Please try rephrasing your question or ask about a different legal topic."
        
        return cleaned
    
    def query(self, question: str, top_k: int = 3) -> Dict:
        """
        Complete RAG query: retrieve + generate
        
        Args:
            question: User question
            top_k: Number of chunks to retrieve
            
        Returns:
            Dict with answer and sources
        """
        logger.info(f"Processing query: {question[:50]}...")
        
        # Retrieve relevant chunks
        retrieved_chunks = self.retrieve(question, top_k=top_k)
        
        if not retrieved_chunks:
            return {
                "answer": "I don't know. Please consult an official authority.",
                "sources": [],
                "raw_answer": "No relevant context found."
            }
        
        # Generate answer
        answer = self.generate_answer(question, retrieved_chunks)
        
        # Format sources
        sources = []
        for chunk in retrieved_chunks:
            sources.append({
                "source": chunk['metadata'].get('source', 'Unknown'),
                "page": chunk['metadata'].get('page', 'Unknown'),
                "snippet": chunk['text'][:200] + "..."
            })
        
        return {
            "answer": answer,
            "sources": sources,
            "raw_answer": answer
        }


# Utility function for standalone testing
if __name__ == "__main__":
    # Initialize pipeline
    rag = RAGPipeline()
    
    # Ingest PDFs
    num_chunks = rag.ingest_pdfs()
    print(f"\nIngested {num_chunks} chunks")
    
    # Test query
    test_query = "What are the basic rights of workers in India?"
    print(f"\nQuery: {test_query}")
    
    result = rag.query(test_query)
    print(f"\nAnswer: {result['answer']}")
    print(f"\nSources:")
    for source in result['sources']:
        print(f"- {source['source']} (Page {source['page']})")
