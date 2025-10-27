# ⚖️ AI Legal Rights Assistant - Enhanced Edition

A powerful AI-powered legal rights education platform that combines **Retrieval-Augmented Generation (RAG)** with **web search** to provide comprehensive, accurate, and up-to-date legal information.

---

## 🌟 Key Features

### Core Capabilities
- **📄 PDF Document Processing**: Automatically ingests and processes legal PDFs
- **🔍 Semantic Search**: Advanced vector search using sentence transformers
- **🌐 Web Search Integration**: Real-time internet search for additional context
- **💾 Conversation History**: Full chat history with conversation management
- **📤 Export Functionality**: Download conversations as JSON
- **⚡ Fast Response**: Optimized for quick answers (< 5 seconds)

### Technical Features
- **100% Offline Capable**: Works without internet (optional web search)
- **Persistent Storage**: ChromaDB stores embeddings locally
- **Grounded Answers**: Responses based on retrieved context
- **Source Citations**: Every answer includes document references
- **Modern UI**: Clean, professional, responsive UI
- **Interactive Chat**: Real-time conversational interface

---

## 🚀 Quick Start

### Windows
```bash
# Run the unified enhanced application
run_unified.bat
```

### Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
streamlit run app_unified.py
```

The application will automatically:
1. Load AI models (first run downloads ~500MB)
2. Ingest PDF documents from `data/` directory
3. Open in browser at `http://localhost:8501`

---

## 📁 Project Structure

```
AI_legal_aid/
├── app_unified.py              # 🆕 Main unified application
├── rag_pipeline_advanced.py    # 🆕 Advanced RAG with web search
├── backend/
│   └── api_enhanced.py         # 🆕 Enhanced FastAPI backend
├── data/                        # Legal PDF documents
├── db/                          # ChromaDB vector store
└── requirements.txt             # Updated dependencies
```

---

## ✨ What's New in Enhanced Edition

### 1. **Web Search Integration** 🌐
- Searches the internet for additional information
- Combines local knowledge with real-time data
- Provides comprehensive, up-to-date answers

### 2. **Enhanced RAG Pipeline** 🚀
- Improved document retrieval
- Better context generation
- Longer, more detailed answers
- Smart chunking and embedding

### 3. **Conversation Management** 💾
- Full conversation history
- Multiple conversation support
- Export conversations as JSON
- Session persistence

### 4. **Modern UI** 🎨
- Professional design with gradients
- Smooth animations
- Responsive layout
- Better mobile support

### 5. **Enhanced Features** ⚡
- Source citations (local + web)
- Processing time metrics
- Clear chat functionality
- Settings panel

---

## 🎯 Usage

### Basic Usage

1. **Launch the app**: Run `run_unified.bat` or `streamlit run app_unified.py`
2. **Wait for initialization**: Models load on first run (2-5 minutes)
3. **Ask your question**: Type in the chat box
4. **Get comprehensive answer**: View answer with sources
5. **Explore sources**: Click to view local and web sources

### Advanced Usage

1. **Enable Web Search**: Toggle in sidebar for internet-enhanced answers
2. **Adjust Sources**: Use slider to retrieve more context
3. **Export Conversation**: Download chat history as JSON
4. **Clear Chat**: Start fresh conversation anytime

---

## 🔧 Configuration

### Web Search
Web search is enabled by default. To disable:
```python
rag_pipeline = AdvancedRAGPipeline(enable_web_search=False)
```

### Number of Sources
Adjust in the sidebar (1-5 sources):
- More sources = more comprehensive but slower
- Recommended: 3 sources for balance

### Models
Current models:
- **Embedding**: `sentence-transformers/all-MiniLM-L6-v2`
- **LLM**: `google/flan-t5-base`

For better quality (requires more RAM):
```python
llm_model="google/flan-t5-large"
```

---

## 📊 Features Comparison

| Feature | Basic Version | Enhanced Version |
|---------|--------------|------------------|
| RAG Retrieval | ✅ | ✅ |
| Web Search | ❌ | ✅ |
| Chat History | ❌ | ✅ |
| Export Chat | ❌ | ✅ |
| Source Citations | ✅ | ✅ |
| UI Quality | Basic | Professional |
| Response Time | 3-5s | 3-5s |
| Answer Quality | Good | Excellent |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit |
| **LLM** | google/flan-t5-base (HuggingFace) |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 |
| **Vector Store** | ChromaDB (persistent) |
| **PDF Processing** | PyPDF |
| **Web Search** | googlesearch-python |

---

## 📖 Example Questions

- "What are the basic rights of workers in India?"
- "How can I file a consumer complaint?"
- "What is the minimum wage law?"
- "What are my digital privacy rights?"
- "How do I get compensation for defective products?"
- "What are the working hours regulations?"

---

## 🔍 How It Works

1. **Document Ingestion** 📄
   - PDFs are loaded and processed
   - Text is extracted and chunked
   - Embeddings are generated using sentence transformers
   - Stored in ChromaDB

2. **Query Processing** 🔍
   - User question is embedded
   - Similar chunks are retrieved from local knowledge base
   - Optional: Web search for additional context
   - Context is combined

3. **Answer Generation** 💡
   - LLM generates comprehensive answer
   - Sources are cited
   - Answer is displayed with citations

4. **History Management** 💾
   - Conversation is saved
   - Can be exported
   - Clear anytime

---

## ⚠️ Important Disclaimer

**THIS IS AN EDUCATIONAL TOOL AND DOES NOT CONSTITUTE LEGAL ADVICE.**

- Information may not be complete or current
- Laws change frequently
- For specific legal matters, consult a qualified attorney
- This is a technical demonstration of AI capabilities

---

## 🐛 Troubleshooting

### "No module named 'xyz'"
```bash
pip install -r requirements.txt
```

### "Slow response times"
- Reduce number of sources in sidebar
- Disable web search for faster responses
- Use a GPU for faster inference

### "Web search not working"
- Install: `pip install googlesearch-python requests`
- Some networks may block web search
- Try disabling web search in settings

### "ChromaDB errors"
- Delete `db/` folder and restart
- Check disk space availability

---

## 🚀 Future Enhancements

- [ ] Multiple language support
- [ ] Voice input/output
- [ ] Mobile app
- [ ] Advanced filtering
- [ ] User authentication
- [ ] Analytics dashboard
- [ ] Model fine-tuning
- [ ] OCR for scanned PDFs

---

## 📝 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/)
- [HuggingFace](https://huggingface.co/)
- [ChromaDB](https://www.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [PyPDF](https://pypdf.readthedocs.io/)

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review code documentation
3. Test with example queries
4. Verify PDF documents are valid

---

**Built with ❤️ for accessible legal information**

*Remember: This is an educational tool. Always seek professional legal advice for your specific situation.*

