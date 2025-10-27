# ⚡ AI Legal Aid Chatbot - Quick Reference Card

## 🚀 Getting Started (30 seconds)

```bash
# Windows: Just double-click
run.bat

# Or manually:
streamlit run app.py
```

**First time?** Run: `python test_setup.py`

---

## 📁 Project Structure

```
ai-legal-aid-chatbot/
├── app.py              ← Streamlit UI
├── rag_pipeline.py     ← RAG logic
├── prompts.py          ← Prompt templates
├── config.py           ← Settings
├── requirements.txt    ← Dependencies
├── data/               ← Your PDFs here
└── db/                 ← Vector database (auto)
```

---

## 🎯 Key Commands

| Command | Purpose |
|---------|---------|
| `streamlit run app.py` | Start the chatbot |
| `python test_setup.py` | Verify installation |
| `python rag_pipeline.py` | Test RAG directly |
| `pip install -r requirements.txt` | Install dependencies |

---

## 💡 Example Questions

```
✅ "What are the basic rights of workers in India?"
✅ "How can I file a consumer complaint?"
✅ "What is the minimum wage law?"
✅ "What are my digital privacy rights?"
✅ "What is the working hours limit?"
```

---

## 🔧 Quick Settings

**In Sidebar:**
- **Sources (1-5)**: More = better context, slower
- **Re-ingest**: Check after adding new PDFs

**In config.py:**
- `DEFAULT_TOP_K = 3` - Number of sources
- `CHUNK_SIZE = 500` - Text chunk size
- `TEMPERATURE = 0.7` - Generation creativity

---

## 📊 Performance

| Metric | Expected |
|--------|----------|
| First query | 3-5 seconds |
| Next queries | 1-3 seconds |
| PDF ingestion | 30-60s per PDF |
| Model loading | 10-30 seconds |

---

## 🐛 Quick Fixes

**App won't start?**
```bash
pip install -r requirements.txt --force-reinstall
```

**Slow responses?**
- Reduce sources to 1-2
- Check CPU usage

**No answers?**
- Check PDFs in data/ folder
- Try re-ingesting (sidebar checkbox)

**Database errors?**
```bash
rmdir /s db  # Windows
rm -rf db    # Linux/Mac
# Then restart app
```

---

## 📚 Documentation

| File | What's Inside |
|------|---------------|
| `README.md` | Complete guide |
| `USAGE_GUIDE.md` | How to use |
| `PROJECT_SUMMARY.md` | Overview |
| `QUICK_REFERENCE.md` | This file |

---

## ⚠️ Remember

- ✅ For **information only**
- ✅ Not **legal advice**
- ✅ Consult a **lawyer** for legal matters
- ✅ Always **verify** information

---

## 🎨 UI Sections

```
┌─────────────────────────────┐
│ ⚖️ Header                   │
├─────────────────────────────┤
│ ⚠️ Disclaimer               │
├─────────────────────────────┤
│ 💬 Query Box                │
│ [🔍 Get Answer] [🗑️ Clear] │
├─────────────────────────────┤
│ 💡 Answer                   │
│ 🔑 Key Points               │
│ 📚 Sources                  │
│ ⏱️ Metrics                  │
└─────────────────────────────┘
```

---

## 🔒 Privacy

- ✅ 100% offline
- ✅ No tracking
- ✅ No external calls
- ✅ Local processing

---

## 📞 Need Help?

1. Check `USAGE_GUIDE.md`
2. Run `test_setup.py`
3. Review error messages
4. Check `README.md` troubleshooting

---

## 🎯 Success Checklist

- [ ] Dependencies installed
- [ ] PDFs in data/ folder
- [ ] App starts without errors
- [ ] First ingestion complete
- [ ] Test query works
- [ ] Sources displayed
- [ ] Response < 3 seconds

---

## 📦 What You Get

- ✅ RAG chatbot (offline)
- ✅ 3 legal PDFs included
- ✅ Beautiful Streamlit UI
- ✅ Source citations
- ✅ Complete documentation
- ✅ Easy setup

---

## 🚀 Next Steps

1. **Verify**: `python test_setup.py`
2. **Start**: `streamlit run app.py`
3. **Wait**: First ingestion (2-5 min)
4. **Ask**: Try example questions
5. **Explore**: Check sources
6. **Customize**: Edit config.py

---

**That's it! You're ready to go! ⚖️**

*For detailed info, see README.md and USAGE_GUIDE.md*
