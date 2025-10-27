# 🏗️ AI Legal Aid Chatbot - System Architecture

## Overview

This document describes the technical architecture of the AI Legal Aid Chatbot.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Streamlit - app.py)                       │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Query Input  │  │   Settings   │  │   Results    │        │
│  │   Box        │  │   Sidebar    │  │   Display    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RAG PIPELINE LAYER                         │
│                   (rag_pipeline.py)                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    RAGPipeline Class                      │ │
│  │                                                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │ │
│  │  │  Ingestion  │  │  Retrieval  │  │ Generation  │     │ │
│  │  │   Module    │  │   Module    │  │   Module    │     │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      STORAGE & MODELS LAYER                     │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   ChromaDB   │  │  Embeddings  │  │     LLM      │        │
│  │  (Vector DB) │  │    Model     │  │    Model     │        │
│  │              │  │              │  │              │        │
│  │  Persistent  │  │  MiniLM-L6   │  │  FLAN-T5     │        │
│  │   Storage    │  │   (80MB)     │  │  (300MB)     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    data/ directory                        │ │
│  │                                                           │ │
│  │  • Labour Laws PDF                                        │ │
│  │  • Consumer Rights PDF                                    │ │
│  │  • Digital Privacy PDF                                    │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Ingestion Phase (One-time)

```
PDF Files (data/)
    │
    ▼
┌─────────────────────┐
│  PDF Reader         │  Extract text page by page
│  (PyPDF)            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Text Chunker       │  Split into 500-char chunks
│  (Custom Logic)     │  with 50-char overlap
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Embedding Model    │  Convert text to vectors
│  (MiniLM-L6-v2)     │  384-dimensional
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ChromaDB           │  Store vectors + metadata
│  (Vector Store)     │  (source, page, text)
└─────────────────────┘
```

### 2. Query Phase (Real-time)

```
User Query
    │
    ▼
┌─────────────────────┐
│  Embedding Model    │  Convert query to vector
│  (MiniLM-L6-v2)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ChromaDB           │  Semantic search
│  (Similarity)       │  Find top-K chunks
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Context Builder    │  Format retrieved chunks
│  (Prompt Template)  │  + user query
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  LLM                │  Generate answer
│  (FLAN-T5-small)    │  based on context
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Response Parser    │  Extract answer,
│  (Custom Logic)     │  key points, sources
└──────────┬──────────┘
           │
           ▼
    Display to User
```

---

## Component Details

### 1. User Interface (app.py)

**Technology**: Streamlit  
**Responsibilities**:
- Render UI components
- Handle user input
- Display results
- Manage settings
- Show disclaimer

**Key Features**:
- Custom CSS styling
- Responsive layout
- Real-time updates
- Progress indicators
- Error handling

### 2. RAG Pipeline (rag_pipeline.py)

**Class**: `RAGPipeline`  
**Responsibilities**:
- Orchestrate RAG workflow
- Manage models
- Handle data processing

**Methods**:
- `__init__()` - Initialize models
- `ingest_pdfs()` - Process PDFs
- `retrieve()` - Semantic search
- `generate_answer()` - LLM generation
- `query()` - End-to-end pipeline

### 3. Prompt Management (prompts.py)

**Responsibilities**:
- Store prompt templates
- Maintain consistency
- Easy modification

**Templates**:
- System prompt
- RAG prompt template
- Disclaimer text

### 4. Configuration (config.py)

**Responsibilities**:
- Centralize settings
- Easy customization
- Default values

**Settings**:
- Model names
- Chunk parameters
- Retrieval settings
- UI configuration

---

## Technology Stack

### Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **UI** | Streamlit | ≥1.28.0 | Web interface |
| **Embeddings** | Sentence Transformers | ≥2.2.2 | Text vectorization |
| **LLM** | Transformers | ≥4.35.0 | Text generation |
| **Vector DB** | ChromaDB | ≥0.4.18 | Similarity search |
| **PDF** | PyPDF | ≥3.17.0 | PDF parsing |
| **ML** | PyTorch | ≥2.1.0 | Model runtime |

### Models

| Model | Size | Purpose | Source |
|-------|------|---------|--------|
| all-MiniLM-L6-v2 | 80MB | Embeddings | HuggingFace |
| flan-t5-small | 300MB | Generation | HuggingFace |

---

## Data Flow Patterns

### Pattern 1: Cold Start (First Run)

```
1. User starts app
2. Load embedding model (10s)
3. Load LLM model (20s)
4. Check for existing DB
5. If no DB: Ingest PDFs (2-5 min)
6. Ready for queries
```

### Pattern 2: Warm Start (Subsequent Runs)

```
1. User starts app
2. Load embedding model (10s)
3. Load LLM model (20s)
4. Load existing DB (instant)
5. Ready for queries
```

### Pattern 3: Query Processing

```
1. User enters query
2. Embed query (0.1s)
3. Search ChromaDB (0.2s)
4. Retrieve top-K chunks (0.1s)
5. Build prompt (0.1s)
6. Generate answer (1-2s)
7. Parse response (0.1s)
8. Display results (instant)
Total: 1-3 seconds
```

---

## Storage Architecture

### ChromaDB Structure

```
db/
├── chroma.sqlite3          # Metadata database
└── [collection_id]/
    ├── data_level0.bin     # Vector data
    ├── header.bin          # Index header
    └── length.bin          # Metadata
```

**Collection Schema**:
```python
{
    "id": "chunk_0",
    "embedding": [0.123, -0.456, ...],  # 384 dims
    "document": "text content...",
    "metadata": {
        "source": "Labour_Handbook.pdf",
        "page": 15
    }
}
```

---

## Security Architecture

### Privacy Measures

1. **No External Calls**
   - All processing local
   - No API requests
   - No telemetry

2. **Data Isolation**
   - PDFs stay on disk
   - Embeddings stored locally
   - No cloud storage

3. **No Logging**
   - Queries not saved
   - No user tracking
   - No analytics

---

## Performance Optimization

### Caching Strategy

1. **Model Caching**
   - Models loaded once
   - Kept in memory
   - Reused across queries

2. **Streamlit Caching**
   - `@st.cache_resource` for models
   - Prevents reloading
   - Faster subsequent runs

3. **Vector Store**
   - Persistent storage
   - No re-embedding
   - Fast similarity search

### Optimization Techniques

1. **Chunking**
   - Optimal size (500 chars)
   - Sentence boundaries
   - Minimal overlap (50 chars)

2. **Retrieval**
   - Top-K limiting (3 default)
   - Distance-based filtering
   - Efficient indexing

3. **Generation**
   - Beam search (4 beams)
   - Early stopping
   - Length limiting

---

## Error Handling

### Error Flow

```
Try:
    Execute operation
Catch:
    Log error
    Show user-friendly message
    Provide recovery steps
Finally:
    Clean up resources
```

### Error Types

1. **Initialization Errors**
   - Model loading failures
   - Missing dependencies
   - Insufficient memory

2. **Ingestion Errors**
   - PDF read failures
   - Encoding issues
   - Storage errors

3. **Query Errors**
   - Empty queries
   - Retrieval failures
   - Generation timeouts

---

## Scalability Considerations

### Current Limits

- **PDFs**: ~50 documents
- **Total Size**: ~500MB
- **Chunks**: ~10,000 chunks
- **Concurrent Users**: 1 (local)

### Scaling Options

1. **More PDFs**
   - Batch ingestion
   - Incremental updates
   - Larger vector DB

2. **Better Models**
   - flan-t5-base (better quality)
   - all-mpnet-base (better embeddings)
   - Requires more RAM

3. **Multi-User**
   - Deploy to server
   - Add authentication
   - Load balancing

---

## Deployment Options

### Option 1: Local (Current)
```
✅ Simple setup
✅ Full privacy
✅ No costs
❌ Single user
❌ Manual updates
```

### Option 2: Docker
```
✅ Portable
✅ Consistent environment
✅ Easy deployment
❌ Requires Docker
```

### Option 3: Cloud
```
✅ Multi-user
✅ Always available
✅ Auto-scaling
❌ Privacy concerns
❌ Hosting costs
```

---

## Monitoring & Metrics

### Built-in Metrics

- Response time
- Number of sources used
- Model loading time
- Ingestion progress

### Potential Additions

- Query success rate
- Average response quality
- User satisfaction
- System resource usage

---

## Future Architecture Enhancements

### Planned Improvements

1. **Caching Layer**
   - Cache frequent queries
   - Faster responses
   - Reduced compute

2. **API Layer**
   - REST API
   - Programmatic access
   - Integration support

3. **Database Upgrades**
   - Hybrid search
   - Metadata filtering
   - Better indexing

4. **Model Improvements**
   - Larger models
   - Fine-tuning
   - Domain adaptation

---

**Architecture Version**: 1.0  
**Last Updated**: October 2025  
**Status**: Production Ready ✅
