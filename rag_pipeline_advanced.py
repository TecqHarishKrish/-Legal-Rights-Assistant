"""
Advanced RAG Pipeline with Web Search Integration
Combines local knowledge base with internet search for comprehensive answers
"""

import os
import logging
from typing import List, Dict, Optional
from pathlib import Path
import re
import json
import requests
from datetime import datetime

# Disable TensorFlow
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

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Web search
WEB_SEARCH_AVAILABLE = False
try:
    from googlesearch import search
    WEB_SEARCH_AVAILABLE = True
    logger.info("Web search enabled")
except ImportError:
    WEB_SEARCH_AVAILABLE = False
    logger.warning("Google search not available. Install with: pip install googlesearch-python")
except Exception as e:
    WEB_SEARCH_AVAILABLE = False
    logger.warning(f"Web search disabled: {str(e)}")

from prompts import RAG_PROMPT_TEMPLATE, SYSTEM_PROMPT


class AdvancedRAGPipeline:
    """
    Advanced RAG pipeline with web search integration
    """
    
    def __init__(
        self,
        data_dir: str = "data",
        db_dir: str = "db",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "google/flan-t5-base",
        chunk_size: int = 600,
        chunk_overlap: int = 100,
        collection_name: str = "legal_docs",
        enable_web_search: bool = True
    ):
        """
        Initialize Advanced RAG pipeline
        """
        self.data_dir = Path(data_dir)
        self.db_dir = Path(db_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.collection_name = collection_name
        self.enable_web_search = enable_web_search and WEB_SEARCH_AVAILABLE
        
        logger.info("Initializing Advanced RAG Pipeline...")
        
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
        
        # Initialize LLM
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
        logger.info(f"Web search: {'Enabled' if self.enable_web_search else 'Disabled'}")
        
        logger.info("Advanced RAG Pipeline initialized successfully!")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,;:!?()\-\'\"]+', '', text)
        return text.strip()
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """Split text into overlapping chunks with metadata"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if len(chunk_text.strip()) > 50:
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
        """Ingest all PDFs from data directory"""
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
        """Retrieve relevant documents for a query with improved relevance"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Query ChromaDB with more results for better filtering
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k * 2, 10)  # Get more candidates
        )
        
        # Format results
        retrieved_docs = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                doc = {
                    'text': results['documents'][0][i],
                    'source': results['metadatas'][0][i].get('source', 'Unknown'),
                    'page': results['metadatas'][0][i].get('page', 'N/A'),
                    'distance': results['distances'][0][i] if 'distances' in results else None
                }
                retrieved_docs.append(doc)
        
        # Filter by relevance - only keep documents that contain keywords from query
        query_keywords = set(query.lower().split())
        relevant_docs = []
        
        for doc in retrieved_docs:
            text_lower = doc['text'].lower()
            # Check if document contains any query keywords
            keywords_found = sum(1 for word in query_keywords if len(word) > 3 and word in text_lower)
            
            # Only include if it has at least some relevance
            if keywords_found > 0 or len(query_keywords) <= 2:
                relevant_docs.append(doc)
        
        # Return top_k most relevant
        return relevant_docs[:top_k] if relevant_docs else retrieved_docs[:top_k]
    
    def web_search(self, query: str, num_results: int = 3) -> List[Dict]:
        """
        Perform web search for additional information
        """
        if not self.enable_web_search:
            return []
        
        try:
            search_results = []
            
            # Perform Google search
            for url in search(query, num_results=num_results, lang='en'):
                try:
                    # Try to extract content from URL
                    response = requests.get(url, timeout=5, headers={
                        'User-Agent': 'Mozilla/5.0'
                    })
                    
                    if response.status_code == 200:
                        # Simple text extraction
                        text = response.text[:1000]  # First 1000 chars
                        search_results.append({
                            'text': text,
                            'source': 'Web Search',
                            'url': url,
                            'page': 'N/A',
                            'distance': None
                        })
                        
                        if len(search_results) >= num_results:
                            break
                except:
                    continue
            
            return search_results
            
        except Exception as e:
            logger.warning(f"Web search failed: {str(e)}")
            return []
    
    def generate_answer(self, query: str, context_docs: List[Dict], web_context: List[Dict] = None) -> str:
        """
        Generate answer using LLM with improved prompting and better relevance
        """
        # Prepare context with better formatting
        context_parts = []
        
        # Add local knowledge base context
        for i, doc in enumerate(context_docs, 1):
            # Use more of the text for better context
            text_snippet = doc['text'][:400] if len(doc['text']) > 400 else doc['text']
            context_parts.append(
                f"Document {i} from {doc['source']} (Page {doc['page']}):\n{text_snippet}"
            )
        
        # Add web search context if available
        if web_context:
            for i, doc in enumerate(web_context, 1):
                text_snippet = doc['text'][:400] if len(doc['text']) > 400 else doc['text']
                context_parts.append(
                    f"Web Source {i}:\n{text_snippet}"
                )
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Create better prompt that forces relevance to the query
        prompt = f"""Based only on the information provided below, answer this question: "{query}"

Relevant Information:
{context}

Important Instructions:
- Answer ONLY using the information provided above
- If the information doesn't directly address the question, say "Based on the available documents..."
- Be specific and cite the document source
- Write in simple, clear language
- Keep the answer focused on what the documents actually say

Answer:"""
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            max_length=1024,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate with better parameters to prevent repetition
        with torch.no_grad():
            outputs = self.llm.generate(
                **inputs,
                max_length=256,  # Reduced to prevent repetition
                min_length=50,
                num_beams=3,  # Reduced from 4
                temperature=0.9,  # Increased for more variation
                do_sample=True,
                top_p=0.95,
                repetition_penalty=2.0,  # Increased from 1.2 to prevent repetition
                length_penalty=0.8,  # Reduced to encourage shorter answers
                early_stopping=True,
                no_repeat_ngram_size=3  # Prevent n-gram repetition
            )
        
        # Decode
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Clean up repetitive content
        answer = self._clean_repetitive_content(answer)
        
        # If answer is too short or repetitive, provide fallback
        if len(answer) < 30 or answer.count('.') < 2:
            answer = "Based on the legal documents provided, this is an important topic. The documents discuss rights and protections under various laws. For specific details about your rights in this area, please consult the relevant legal documents or speak with a qualified legal professional who can provide guidance based on your specific circumstances."
        
        return answer
    
    def _clean_repetitive_content(self, text: str) -> str:
        """Remove repetitive content from generated text"""
        sentences = text.split('.')
        if len(sentences) < 2:
            return text
        
        # Remove exact duplicates
        unique_sentences = []
        seen = set()
        for sentence in sentences:
            sentence_clean = sentence.strip()
            if sentence_clean and sentence_clean not in seen:
                unique_sentences.append(sentence)
                seen.add(sentence_clean)
        
        # If we have too many similar sentences, take only first few
        if len(unique_sentences) > 5:
            # Check for similarity
            unique_sentences = unique_sentences[:5]
        
        return '. '.join(unique_sentences)
    
    def query(self, question: str, top_k: int = 3, use_web_search: bool = False) -> Dict:
        """
        Complete RAG query: retrieve + generate + optional web search
        """
        try:
            # Expand query with synonyms for better retrieval
            expanded_query = self._expand_query(question)
            
            # Retrieve from local knowledge base
            logger.info(f"Retrieving top {top_k} documents for: {question}")
            retrieved_docs = self.retrieve(expanded_query, top_k=top_k)
            
            # If no relevant docs, try with original query
            if not retrieved_docs:
                retrieved_docs = self.retrieve(question, top_k=top_k)
            
            # Optionally perform web search
            web_docs = []
            if use_web_search and self.enable_web_search:
                logger.info("Performing web search...")
                web_docs = self.web_search(question, num_results=2)
            
            if not retrieved_docs and not web_docs:
                return {
                    'answer': f"I couldn't find specific information about '{question}' in the legal documents. The documents cover topics like worker rights, consumer protection, and digital privacy. Please try asking about: worker rights in India, consumer complaint filing procedures, labor laws, or product safety regulations.",
                    'sources': [],
                    'web_sources': []
                }
            
            # Generate answer
            logger.info("Generating answer...")
            answer = self.generate_answer(question, retrieved_docs, web_docs)
            
            # Check if answer is relevant
            if not self._is_answer_relevant(answer, question):
                answer = f"Based on the legal documents available, here's what I found: {answer}"
            
            # Format sources
            sources = [
                {
                    'source': doc['source'],
                    'page': doc['page'],
                    'snippet': doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text']
                }
                for doc in retrieved_docs
            ]
            
            # Format web sources
            web_sources = [
                {
                    'source': doc.get('url', 'Web Source'),
                    'page': 'N/A',
                    'snippet': doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text']
                }
                for doc in web_docs
            ]
            
            return {
                'answer': answer,
                'sources': sources,
                'web_sources': web_sources,
                'used_web_search': len(web_docs) > 0
            }
            
        except Exception as e:
            logger.error(f"Error in query: {str(e)}")
            return {
                'answer': f"I encountered an error: {str(e)}. Please try rephrasing your question.",
                'sources': [],
                'web_sources': [],
                'error': str(e)
            }
    
    def _expand_query(self, query: str) -> str:
        """Add synonyms to query for better retrieval"""
        expansions = {
            'rights': ['rights', 'protection', 'entitlements'],
            'worker': ['worker', 'employee', 'labor'],
            'consumer': ['consumer', 'customer', 'buyer'],
            'law': ['law', 'regulation', 'act', 'legislation'],
        }
        
        query_lower = query.lower()
        expanded_terms = [query]
        
        for term, synonyms in expansions.items():
            if term in query_lower:
                for syn in synonyms:
                    if syn not in query_lower:
                        expanded_terms.append(query.replace(term, syn))
        
        return " ".join(expanded_terms)
    
    def _is_answer_relevant(self, answer: str, question: str) -> bool:
        """Check if answer is relevant to the question"""
        question_keywords = set(question.lower().split())
        answer_lower = answer.lower()
        
        # Count matching keywords
        matches = sum(1 for word in question_keywords if word in answer_lower and len(word) > 2)
        
        # Answer is relevant if at least 30% of keywords appear
        relevance_ratio = matches / len(question_keywords) if question_keywords else 0
        return relevance_ratio >= 0.3

