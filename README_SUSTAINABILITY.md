# ♻️ AI Sustainability Advisor

A Retrieval-Augmented Generation (RAG) chatbot that provides waste sorting and recycling advice using free, open-source PDF guidelines.

## 🎯 Overview

This application uses local AI models to answer questions about recycling and waste management by retrieving relevant information from government, NGO, or UN sustainability documents.

### Key Features

- 📄 **PDF Ingestion** - Process waste management guideline PDFs
- 🔍 **Semantic Retrieval** - Find relevant information using embeddings
- 🤖 **Local Inference** - Uses FLAN-T5-small model (fully offline)
- 📚 **Grounded Answers** - Answers based on document content
- 🌐 **Streamlit UI** - Clean, user-friendly interface
- ⚠️ **Disclaimer Display** - Always shows compliance notice

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **Libraries:** LangChain, HuggingFace Transformers, SentenceTransformers, ChromaDB, PyPDF, Streamlit
- **Embeddings Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **LLM Model:** `google/flan-t5-small` (free & lightweight)
- **Vector Store:** ChromaDB (persistent, local)

## 📦 Installation

### 1. Clone or Navigate to Project

```bash
cd ai-sustainability-advisor
```

### 2. Install Dependencies

```bash
pip install -r requirements_sustainability.txt
```

### 3. Prepare Data Directory

```bash
mkdir data_sustainability
```

Download waste management guideline PDFs and place them in `data_sustainability/`:
- Government recycling guides
- NGO waste management handbooks
- UN sustainability documents
- Local authority guidelines

## 🚀 Usage

### Launch the Application

```bash
streamlit run app_sustainability.py
```

### Workflow

1. **Initialize System** - Click "Initialize System" in the sidebar
2. **Add PDFs** - Place waste management PDFs in `data_sustainability/` folder
3. **Ask Questions** - Type your question about recycling/waste
4. **Get Answers** - Receive grounded responses with sources

### Example Queries

- "Where should I throw an old charger?"
- "Can I recycle pizza boxes?"
- "How to dispose batteries safely?"
- "What can go in the compost bin?"
- "Can I recycle plastic bags?"

## 📁 Project Structure

```
ai-sustainability-advisor/
│
├── data_sustainability/        # PDF guidelines (add your files here)
│   └── waste_guide.pdf
│
├── db_sustainability/          # ChromaDB persistence (auto-created)
│   ├── chroma.sqlite3
│   └── ...
│
├── app_sustainability.py       # Streamlit app
├── rag_pipeline_sustainability.py  # RAG logic
├── prompts_sustainability.py   # Prompt templates
├── requirements_sustainability.txt  # Dependencies
└── README_SUSTAINABILITY.md    # This file
```

## 🔧 How It Works

### 1. Data Ingestion

- PDFs in `/data_sustainability` are loaded
- Documents split into chunks (~500 tokens)
- Chunks embedded using `all-MiniLM-L6-v2`
- Stored in ChromaDB with metadata (document, page)

### 2. RAG Pipeline

1. User enters query in Streamlit
2. System retrieves top-3 relevant passages from ChromaDB
3. FLAN-T5-small generates grounded response
4. Output formatted (Answer + Key Points + Sources)

### 3. Prompt Template

The system uses this template for generation:

```
You are a sustainability advisor. Answer only using the provided context. 
If the context does not contain the answer, say: "I don't know. Please 
consult your local waste management authority." Always cite your sources. 
Keep answers simple and actionable.
```

## ⚙️ Configuration

### Changing Models

Edit `rag_pipeline_sustainability.py`:

```python
# For embeddings
model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

# For LLM
model="google/flan-t5-small"  # Can use other FLAN models
```

### Adjusting Retrieval

```python
# Retrieve more/fewer documents
result = rag_pipeline.query(query, RAG_PROMPT_TEMPLATE, k=5)
```

## 🎯 Success Criteria

- ✅ **Retrieval accuracy** ≥ 80% (answers reference correct PDF sections)
- ✅ **Response latency** < 3 seconds
- ✅ **Fully offline** (no API costs)
- ✅ **Disclaimer always shown** (compliance notice)

## ⚠️ Important Disclaimers

**This tool provides general recycling guidance. Follow local laws for compliance.**

- Always verify with local waste management authorities
- Regulations vary by location
- When in doubt, contact local experts
- This is not legal or professional advice

## 🐛 Troubleshooting

### No PDF files found

- Ensure `data_sustainability/` directory exists
- Add at least one PDF file to the directory
- Check file extensions are `.pdf`

### Model loading errors

- Ensure you have internet connection for first-time download
- Models download automatically from HuggingFace
- Check available disk space (~2GB for models)

### ChromaDB errors

- Delete `db_sustainability/` folder and re-initialize
- Ensure write permissions in project directory

### Generation issues

- FLAN-T5-small is lightweight; adjust chunk size if needed
- Query length may affect results
- Try rephrasing questions

## 📚 Model Information

### Embeddings: all-MiniLM-L6-v2
- 384 dimensions
- Fast inference
- Good for semantic search

### LLM: FLAN-T5-small
- 80M parameters
- Fast generation
- Good instruction following
- Fine-tuned on multiple tasks

## 🤝 Contributing

To improve the sustainability advisor:

1. Add more PDF documents to knowledge base
2. Fine-tune prompts for better answers
3. Experiment with different embedding models
4. Add support for images/diagrams
5. Implement multi-language support

## 📄 License

This project uses open-source models and libraries. Please check individual licenses:
- LangChain: MIT
- Transformers: Apache 2.0
- SentenceTransformers: Apache 2.0
- ChromaDB: Apache 2.0

## 🙏 Acknowledgments

- HuggingFace for model hosting
- LangChain for RAG framework
- ChromaDB for vector storage
- Streamlit for UI framework

---

**Built with ♻️ for a sustainable future**

