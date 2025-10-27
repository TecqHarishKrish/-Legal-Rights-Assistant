# 🏗️ Architecture: AI Sustainability Advisor

## System Overview

The AI Sustainability Advisor is a Retrieval-Augmented Generation (RAG) system that provides recycling and waste management advice using local AI models and PDF documents.

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│                  (Streamlit Web App)                         │
│  • Query Input                                              │
│  • Answer Display                                           │
│  • Sources & Key Points                                     │
│  • Disclaimer                                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   RAG PIPELINE                              │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐│
│  │  Query         │→ │  Embeddings    │→ │  ChromaDB     ││
│  │  Encoding      │  │  (MiniLM-L6)   │  │  Retrieval    ││
│  └────────────────┘  └────────────────┘  └───────┬─────────┘│
│                                                  │          │
│                                                  ▼          │
│                                      ┌──────────────────┐  │
│                                      │  Context Builder  │  │
│                                      └─────────┬────────┘  │
│                                                │          │
│  ┌────────────────┐  ┌────────────────┐      │          │
│  │  Prompt        │→ │  FLAN-T5-Small │←─────┘          │
│  │  Template      │  │  Generator     │                  │
│  └────────────────┘  └────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  KNOWLEDGE BASE                              │
│  • PDF Documents (data_sustainability/)                     │
│  • ChromaDB Vector Store (db_sustainability/)               │
│  • Metadata (document, page, chunk_index)                   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Document Ingestion (`rag_pipeline_sustainability.py`)

**Process:**
1. Load PDF files from `data_sustainability/`
2. Split into chunks (~500 tokens, 50 token overlap)
3. Generate embeddings using `all-MiniLM-L6-v2`
4. Store in ChromaDB with metadata

**Code:**
```python
SustainabilityRAGPipeline.ingest_pdfs()
```

### 2. Retrieval System

**Embeddings Model:** `sentence-transformers/all-MiniLM-L6-v2`
- 384-dimensional vectors
- Cosine similarity for retrieval
- Fast inference (~50ms per query)

**Retrieval:**
```python
SustainabilityRAGPipeline.retrieve(query, k=3)
```
- Returns top-k relevant passages
- Includes metadata (document, page)

### 3. Generation System

**Model:** `google/flan-t5-small`
- 80M parameters
- Instruction-tuned
- Fast generation (~200ms)
- Fully local (no API calls)

**Process:**
```python
SustainabilityRAGPipeline.generate_answer(query, context, prompt)
```

### 4. Prompt Engineering

**System Prompt:**
```
You are a sustainability advisor. Answer only using the provided context.
If the context does not contain the answer, say: "I don't know. Please
consult your local waste management authority." Always cite your sources.
Keep answers simple and actionable.
```

**Template:**
```
Answer the question based only on the following context about recycling
and waste management.

Context: {context}

Question: {query}

Answer:
```

## Data Flow

```
PDF Files → PyPDF Loader → Text Splitter → Embeddings → ChromaDB
                                                              ↓
User Query → Embeddings → ChromaDB Query → Top-k Context
                                                              ↓
Context + Query → Prompt Template → FLAN-T5 → Generated Answer
                                                              ↓
Answer + Key Points + Sources → Streamlit UI → User
```

## Storage Architecture

```
db_sustainability/
├── chroma.sqlite3          # SQLite database
└── [collection]/            # Vector collection
    ├── data_level0.bin      # Embedding vectors
    ├── header.bin           # Metadata header
    ├── length.bin           # Document lengths
    └── link_lists.bin       # Index structure
```

## Key Design Decisions

### Why FLAN-T5-small?
- Lightweight (80M params)
- Fast inference
- Good instruction following
- No API costs

### Why ChromaDB?
- Persistent storage
- Local deployment
- Easy retrieval
- Good Python API

### Why sentence-transformers?
- Open-source
- Fast embeddings
- Good semantic search
- No API limits

### Why LangChain?
- Standard RAG patterns
- Document loaders
- Text splitters
- Industry standard

## Performance Characteristics

### Ingestion
- Time: ~5-10 seconds per PDF page
- Memory: ~2GB for models
- Storage: ~10MB per 1000 chunks

### Retrieval
- Latency: ~200ms
- Accuracy: ~80% (depends on embeddings quality)

### Generation
- Latency: ~500ms
- Quality: Good for factual queries
- Limitations: Short answers (~100 tokens)

## Scaling Considerations

### Current Setup
- Best for: Small-medium documents (<10 PDFs)
- Users: Single user
- Queries: ~10/minute max

### Future Improvements
1. **Parallel Ingestion** - Process multiple PDFs simultaneously
2. **Larger Models** - Upgrade to FLAN-T5-base or larger
3. **Caching** - Cache common queries
4. **Multi-user** - Add user sessions
5. **Feedback Loop** - Improve based on user feedback

## Security & Privacy

- ✅ Fully local (no data sent to external APIs)
- ✅ PDFs stored locally
- ✅ No tracking or logging
- ✅ User data stays on device

## Limitations

1. **Model Size** - FLAN-T5-small has limitations
   - Short answers
   - May miss nuanced questions
   - Best for factual retrieval

2. **Context Window** - Limited to retrieved chunks
   - May miss relevant info outside top-k
   - Can't process full documents

3. **PDF Quality** - Depends on PDF structure
   - Scanned images need OCR
   - Tables may not parse well
   - Complex layouts may lose information

## Deployment Options

### Local Development
```bash
streamlit run app_sustainability.py
```

### Production
```bash
# Using Streamlit Cloud
streamlit deploy

# Or Docker
docker run -p 8501:8501 sustainability-app
```

### Self-Hosted
- No API key needed
- Fully offline
- Privacy preserving

---

**Built for sustainability with local-first AI** ♻️

