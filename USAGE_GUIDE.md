# 📘 AI Legal Aid Chatbot - Usage Guide

## Quick Start

### Windows Users
Simply double-click `run.bat` - it will:
1. Create a virtual environment (if needed)
2. Install dependencies (if needed)
3. Launch the application

### Manual Start
```bash
# 1. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Run the application
streamlit run app.py
```

---

## First Time Setup

### 1. Verify Installation
```bash
python test_setup.py
```

This will check:
- ✅ All dependencies are installed
- ✅ Project structure is correct
- ✅ PDF files are present
- ✅ Models can be loaded

### 2. Initial Run
On first run, the application will:
1. **Load models** (~30 seconds)
   - Embedding model: all-MiniLM-L6-v2
   - LLM model: flan-t5-small

2. **Ingest PDFs** (~2-5 minutes)
   - Extract text from PDFs
   - Create text chunks
   - Generate embeddings
   - Store in ChromaDB

3. **Ready to use!**

---

## Using the Chatbot

### Main Interface

```
┌─────────────────────────────────────────┐
│  ⚖️ AI Legal Aid Chatbot                │
│  Get information about Labour Laws,     │
│  Consumer Rights & Digital Privacy      │
├─────────────────────────────────────────┤
│  ⚠️ DISCLAIMER                          │
│  For informational purposes only        │
├─────────────────────────────────────────┤
│  💬 Ask Your Question                   │
│  ┌─────────────────────────────────┐   │
│  │ Enter your question here...     │   │
│  └─────────────────────────────────┘   │
│  [🔍 Get Answer] [🗑️ Clear]            │
└─────────────────────────────────────────┘
```

### Asking Questions

**Good Questions:**
- ✅ "What are the basic rights of workers in India?"
- ✅ "How can I file a consumer complaint?"
- ✅ "What is the minimum wage law?"
- ✅ "What are my digital privacy rights?"

**Avoid:**
- ❌ Too vague: "Tell me about laws"
- ❌ Too specific: "What's the law in case XYZ-123-ABC?"
- ❌ Personal advice: "Should I sue my employer?"

### Understanding Responses

Each answer includes:

#### 1. Answer Section
```
💡 Answer
A clear 3-5 sentence explanation based on 
the retrieved documents.
```

#### 2. Key Points
```
🔑 Key Points
- Important point 1
- Important point 2
- Important point 3
```

#### 3. Sources
```
📚 Sources
📄 Consumer_Handbook.pdf - Page 15
   Snippet: "Consumers have the right to..."

📄 Labour Handbook.pdf - Page 23
   Snippet: "Workers are entitled to..."
```

---

## Sidebar Features

### Information Panel
- **About**: Overview of the chatbot
- **Features**: List of capabilities
- **Knowledge Base**: Shows loaded PDF files

### Settings

#### Number of Sources (1-5)
- **Lower (1-2)**: Faster, more focused
- **Higher (4-5)**: More context, slower

**Recommended**: 3 (default)

#### Force Re-ingest PDFs
Check this when:
- ✅ You added new PDF files
- ✅ You updated existing PDFs
- ✅ Database seems corrupted

**Note**: Re-ingestion takes 2-5 minutes

---

## Advanced Usage

### Adding New Documents

1. **Place PDF in data/ folder**
   ```
   data/
   ├── existing_doc1.pdf
   ├── existing_doc2.pdf
   └── new_document.pdf  ← Add here
   ```

2. **Re-ingest documents**
   - Open sidebar
   - Check "Force re-ingest PDFs"
   - Wait for processing

3. **Verify**
   - Check sidebar "Knowledge Base" section
   - New document should be listed

### Customizing Behavior

Edit `config.py` to customize:

```python
# Retrieval quality
DEFAULT_TOP_K = 3  # More = better context

# Chunk size
CHUNK_SIZE = 500   # Larger = more context per chunk

# Generation quality
NUM_BEAMS = 4      # Higher = better quality
TEMPERATURE = 0.7  # Lower = more focused
```

### Running Tests

```bash
# Test setup
python test_setup.py

# Test RAG pipeline directly
python rag_pipeline.py
```

---

## Performance Tips

### For Faster Responses
1. Reduce number of sources (1-2)
2. Use smaller chunk size (300-400)
3. Reduce NUM_BEAMS in config (2-3)

### For Better Quality
1. Increase number of sources (4-5)
2. Use larger chunk size (600-800)
3. Increase NUM_BEAMS in config (5-6)
4. Consider using flan-t5-base model

### For Lower Memory Usage
1. Keep default flan-t5-small model
2. Process PDFs in batches
3. Reduce chunk overlap (25-30)

---

## Troubleshooting

### Application Won't Start

**Check Python version:**
```bash
python --version  # Should be 3.8+
```

**Reinstall dependencies:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Slow First Query

**Normal behavior:**
- First query loads models into memory
- Subsequent queries are much faster
- Wait 30-60 seconds for first response

### No Relevant Answers

**Possible causes:**
1. Question not covered in PDFs
2. Too few sources retrieved
3. Poor PDF quality (scanned images)

**Solutions:**
- Rephrase question
- Increase number of sources
- Add more relevant PDFs

### ChromaDB Errors

**Reset database:**
```bash
# Delete database folder
rmdir /s db  # Windows
rm -rf db    # Linux/Mac

# Restart application
streamlit run app.py
```

### Memory Errors

**Reduce memory usage:**
1. Close other applications
2. Use smaller model (flan-t5-small)
3. Reduce batch size in config
4. Process fewer PDFs at once

---

## Best Practices

### For Users

1. **Be Specific**: Ask clear, focused questions
2. **Check Sources**: Always review source citations
3. **Verify Information**: Cross-reference with official sources
4. **Seek Professional Help**: For legal matters, consult a lawyer

### For Administrators

1. **Quality PDFs**: Use official, authoritative documents
2. **Regular Updates**: Keep documents current
3. **Monitor Performance**: Track response times
4. **User Feedback**: Collect and address user concerns

---

## Example Workflows

### Workflow 1: Research Worker Rights

1. Ask: "What are the basic rights of workers?"
2. Review answer and key points
3. Check sources for specific laws
4. Ask follow-up: "What is the minimum wage?"
5. Compare information across sources

### Workflow 2: Consumer Complaint

1. Ask: "How do I file a consumer complaint?"
2. Note the key points (steps)
3. Check source documents for forms
4. Ask: "What documents do I need?"
5. Compile information for action

### Workflow 3: Privacy Rights

1. Ask: "What are my digital privacy rights?"
2. Review applicable laws
3. Ask: "How can I protect my data?"
4. Check sources for official guidelines
5. Implement recommendations

---

## Keyboard Shortcuts

When in Streamlit:
- `Ctrl + R`: Reload page
- `Ctrl + Shift + R`: Hard reload (clear cache)
- `Ctrl + C`: Stop server (in terminal)

---

## Getting Help

### Check These First
1. ✅ README.md - Complete documentation
2. ✅ This guide - Usage instructions
3. ✅ test_setup.py - Verify installation
4. ✅ Troubleshooting section above

### Still Need Help?
1. Check error messages carefully
2. Verify all files are present
3. Ensure PDFs are valid (not scanned)
4. Try with example questions first

---

## Updates and Maintenance

### Updating Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Backing Up Data
```bash
# Backup database
copy db backup_db  # Windows
cp -r db backup_db  # Linux/Mac

# Backup PDFs
copy data backup_data  # Windows
cp -r data backup_data  # Linux/Mac
```

### Cleaning Up
```bash
# Remove cache
rmdir /s __pycache__  # Windows
rm -rf __pycache__    # Linux/Mac

# Remove database (will re-ingest on next run)
rmdir /s db  # Windows
rm -rf db    # Linux/Mac
```

---

## Security Notes

- ✅ All processing is local (offline)
- ✅ No data sent to external servers
- ✅ No user tracking or analytics
- ✅ PDFs stay on your machine
- ✅ Queries are not logged

---

## Performance Benchmarks

**Typical Performance:**
- Initial setup: 2-5 minutes
- First query: 3-5 seconds
- Subsequent queries: 1-3 seconds
- PDF ingestion: 30-60 seconds per PDF

**Hardware Requirements:**
- Minimum: 4GB RAM, Dual-core CPU
- Recommended: 8GB RAM, Quad-core CPU
- Storage: 2GB for models + PDF size

---

**Happy querying! Remember: This is for information only, not legal advice.** ⚖️
