# 🚀 Quick Start Guide - Enhanced AI Legal Assistant

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)
```bash
# Install required packages
pip install -r requirements.txt
```

**What gets installed:**
- Streamlit (web framework)
- Transformers & PyTorch (AI models)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- FastAPI & Uvicorn (optional backend)
- Google Search (web search)

---

## 🎯 Step 2: Run the Application (1 minute)

### Windows:
```bash
run_unified.bat
```

### Linux/Mac:
```bash
streamlit run app_unified.py
```

### What happens:
1. ✅ Streamlit opens browser automatically
2. ✅ AI models load (first time: ~500MB download)
3. ✅ PDFs from `data/` are processed
4. ✅ Ready to use!

---

## 💬 Step 3: Ask Your First Question (1 minute)

### Try these questions:
1. "What are the basic rights of workers in India?"
2. "How can I file a consumer complaint?"
3. "What is the minimum wage law?"
4. "What are my digital privacy rights?"

### Features to explore:
- ✅ Enable web search for real-time info
- ✅ View sources (local + web)
- ✅ Export conversation as JSON
- ✅ Clear chat to start fresh
- ✅ Adjust sources (1-5)

---

## 🎨 What You'll See

### Hero Section
- Professional gradient header
- Feature highlights
- Mission statement

### Disclaimer
- Important legal notice
- Dismissible

### Chat Interface
- Interactive chatbot
- Message bubbles
- Source citations
- Loading animations

### Sidebar
- Settings
- Document list
- Clear chat button
- Export conversation
- Feature info

---

## 🔧 Troubleshooting

### Problem: "No module named 'xyz'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Web search not working
**Solution:**
```bash
pip install googlesearch-python requests
```

### Problem: Slow first response
**Solution:**
- Normal - models load first time
- Subsequent queries are fast
- Takes 2-5 minutes first run

### Problem: Out of memory
**Solution:**
- Close other applications
- Use smaller model: `google/flan-t5-small`
- Reduce chunk size in code

---

## 📊 System Requirements

### Minimum:
- CPU: Intel i5 / AMD Ryzen 5
- RAM: 8GB
- Storage: 2GB free
- Python: 3.8+

### Recommended:
- CPU: Intel i7 / AMD Ryzen 7
- RAM: 16GB
- Storage: 5GB free (for models)
- GPU: Optional (faster inference)

---

## 🎯 Usage Tips

### For Best Results:
1. ✅ Ask specific questions
2. ✅ Enable web search for current info
3. ✅ Use 3-5 sources for comprehensive answers
4. ✅ Check sources for verification
5. ✅ Export important conversations

### Answer Quality:
- **1 source**: Quick answer
- **3 sources**: Balanced (recommended)
- **5 sources**: Comprehensive

### With Web Search:
- More up-to-date information
- Combines local + internet knowledge
- Takes slightly longer
- More comprehensive answers

---

## 🚀 Advanced Usage

### Using the Backend API

```bash
# Start backend
cd backend
python api_enhanced.py

# Test API
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are worker rights?", "use_web_search": true}'
```

### Custom Configuration

Edit `app_unified.py`:
```python
# Change model
llm_model="google/flan-t5-large"  # Better quality

# Disable web search
enable_web_search=False

# Change chunk size
chunk_size=800
chunk_overlap=150
```

---

## 📖 What's Different from Basic Version?

| Feature | Basic | Enhanced |
|---------|-------|----------|
| Web Search | ❌ | ✅ |
| Chat History | ❌ | ✅ |
| Export Chat | ❌ | ✅ |
| UI Quality | Basic | Professional |
| Settings | Minimal | Full Panel |
| Sources | Local only | Local + Web |

---

## 🎓 Learning Resources

### Understanding the System
1. **RAG** - Retrieval-Augmented Generation
2. **Embeddings** - Text to vector conversion
3. **Vector Search** - Find similar documents
4. **LLM** - Generate answers
5. **Web Search** - Additional context

### Key Files
- `app_unified.py` - Main application
- `rag_pipeline_advanced.py` - AI logic
- `backend/api_enhanced.py` - REST API
- `data/` - Your PDF documents
- `db/` - Vector database

---

## ✅ Success Checklist

After setup, you should have:
- [x] Streamlit app running
- [x] Models loaded
- [x] PDFs processed
- [x] Chat interface visible
- [x] Can ask questions
- [x] Get answers with sources
- [x] Export conversations
- [x] Clear chat works

---

## 🎉 You're Ready!

Start asking questions and explore the features. The system is designed to provide comprehensive legal information with proper citations.

**Remember**: This is an educational tool. For specific legal advice, consult a qualified attorney.

---

*Happy exploring! 🚀*

