# 🚀 Quick Start Guide: AI Sustainability Advisor

## Setup in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements_sustainability.txt
```

This installs:
- Streamlit (UI framework)
- LangChain (RAG framework)
- ChromaDB (vector database)
- Sentence-Transformers (embeddings)
- Transformers (LLM models)
- PyPDF (PDF processing)

### Step 2: Add PDF Documents

1. Create or use the `data_sustainability/` folder
2. Download waste management PDFs:
   - Government recycling guides
   - NGO waste management handbooks
   - UN sustainability documents
   - Local authority guidelines
3. Copy PDFs into `data_sustainability/` folder

**Sample Sources:**
- EPA recycling guidelines
- UN Environment Programme documents
- Local municipality waste guides
- NGO sustainability handbooks

### Step 3: Launch Application

**Windows:**
```bash
start_sustainability.bat
```

**Mac/Linux:**
```bash
streamlit run app_sustainability.py
```

Then open browser to `http://localhost:8501`

## Using the App

### 1. Initialize System
- Click "🚀 Initialize System" in sidebar
- Wait for PDF ingestion (may take 1-2 minutes)
- See success message when ready

### 2. Ask Questions
Enter queries like:
- "Where should I throw an old charger?"
- "Can I recycle pizza boxes?"
- "How to dispose batteries safely?"

### 3. Get Answers
Receive:
- **Answer** - Direct response
- **Key Points** - Bullet summary
- **Sources** - Document references with page numbers

## Troubleshooting

### "No PDF files found"
- Ensure `data_sustainability/` folder exists
- Add at least one PDF file
- Check file has `.pdf` extension

### Model Download Issues
- Requires internet for first-time download
- Models are ~2GB total
- Ensure stable connection

### Import Errors
```bash
# Reinstall packages
pip install --upgrade -r requirements_sustainability.txt
```

### ChromaDB Errors
```bash
# Delete and recreate database
rm -rf db_sustainability/
# Then re-initialize in app
```

## File Structure

```
ai-sustainability-advisor/
│
├── data_sustainability/        # ← ADD YOUR PDFs HERE
│   ├── recycling_guide.pdf
│   └── waste_management.pdf
│
├── app_sustainability.py       # Main Streamlit app
├── rag_pipeline_sustainability.py  # RAG logic
├── prompts_sustainability.py   # Prompt templates
├── requirements_sustainability.txt  # Dependencies
└── start_sustainability.bat    # Launch script
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Add PDF documents
3. ✅ Initialize system
4. ✅ Start asking questions!

## ⚠️ Important

**This tool provides general recycling guidance. Follow local laws for compliance.**

Always verify with local waste management authorities for specific regulations.

---

**Ready to go?** Run `streamlit run app_sustainability.py` and click "Initialize System"! ♻️

