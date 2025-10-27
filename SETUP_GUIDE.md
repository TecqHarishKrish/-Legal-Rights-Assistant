# Legal Rights Education Platform - Complete Setup Guide

## 🎯 Overview

This is a professional, modern web application designed to educate citizens about their legal rights in India. It uses AI-powered RAG (Retrieval-Augmented Generation) to provide accurate, source-based answers.

### Key Features
- ✅ **Modern UI**: Built with Next.js, React, and Tailwind CSS
- ✅ **AI-Powered**: Uses HuggingFace models for intelligent responses
- ✅ **Source-Based**: All answers cite official legal documents
- ✅ **Professional Design**: Clean, accessible, mobile-responsive
- ✅ **Social Welfare**: Free educational tool for all citizens

---

## 📋 Prerequisites

### Required Software
1. **Python 3.9+** - [Download](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download](https://nodejs.org/)
3. **Git** - [Download](https://git-scm.com/)

### System Requirements
- RAM: 8GB minimum (16GB recommended)
- Storage: 5GB free space
- Internet: For initial setup only

---

## 🚀 Quick Start (Streamlit Version)

### Step 1: Install Python Dependencies

```bash
cd h:\AI_legal_aid
pip install -r requirements.txt
```

### Step 2: Run the Enhanced Streamlit App

```bash
streamlit run app_enhanced.py
```

The app will open at `http://localhost:8501`

**Features:**
- ✅ Fixed disclaimer visibility (dark text on light background)
- ✅ Auto-clearing chat input after sending
- ✅ Better error handling
- ✅ Professional social welfare design
- ✅ Improved AI responses

---

## 🌐 Full Stack Setup (Next.js + FastAPI)

### Backend Setup

#### 1. Install Python Dependencies

```bash
cd h:\AI_legal_aid
pip install fastapi uvicorn python-multipart
```

#### 2. Update requirements.txt

Add these lines to `requirements.txt`:
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
```

#### 3. Start the FastAPI Backend

```bash
cd h:\AI_legal_aid\backend
python api.py
```

The API will run at `http://localhost:8000`

**API Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `POST /api/ask` - Ask a question
- `GET /api/documents` - List loaded documents
- `GET /docs` - Interactive API documentation

### Frontend Setup

#### 1. Install Node.js Dependencies

```bash
cd h:\AI_legal_aid\frontend
npm install
```

#### 2. Create Environment File

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 3. Start the Development Server

```bash
npm run dev
```

The frontend will run at `http://localhost:3000`

#### 4. Build for Production

```bash
npm run build
npm start
```

---

## 📁 Project Structure

```
h:\AI_legal_aid\
├── data/                          # PDF legal documents
│   ├── Consumer_Handbook.pdf
│   ├── India Handbook of Labour.pdf
│   └── 2bf1fbe5fbe5c8e4f5e4f3e4f2a3b.pdf
├── db/                            # Vector database (auto-generated)
├── backend/                       # FastAPI backend
│   └── api.py
├── frontend/                      # Next.js frontend
│   ├── app/
│   │   ├── page.tsx              # Main chat interface
│   │   ├── layout.tsx            # Layout component
│   │   └── globals.css           # Global styles
│   ├── package.json
│   └── tailwind.config.js
├── app_enhanced.py                # Enhanced Streamlit app
├── rag_pipeline_enhanced.py       # Improved RAG pipeline
├── prompts.py                     # AI prompts
└── requirements.txt               # Python dependencies
```

---

## 🎨 UI/UX Improvements

### Fixed Issues ✅
1. **Disclaimer Visibility**: Changed to dark text (#5a4a0a) on light background (#fffbeb)
2. **Auto-Clear Input**: Chat input clears automatically after sending
3. **Error Handling**: Better error messages and recovery
4. **Professional Design**: Modern gradient colors, smooth animations
5. **Mobile Responsive**: Works on all screen sizes

### Design Philosophy
- **Accessibility**: High contrast, readable fonts
- **Social Welfare**: Welcoming, educational tone
- **Professional**: Clean, trustworthy appearance
- **User-Friendly**: Intuitive navigation, clear CTAs

---

## 🤖 AI Model Improvements

### Enhanced RAG Pipeline

**Improvements:**
1. **Better Chunking**: Larger chunks (600 words) with more overlap (100 words)
2. **Improved Generation**: Using `flan-t5-base` instead of `flan-t5-small`
3. **Better Prompts**: More structured, detailed responses
4. **Error Recovery**: Graceful handling of edge cases

### Generation Parameters
```python
max_length=512          # Longer, more detailed answers
num_beams=4            # Better quality
temperature=0.7        # Balanced creativity
top_p=0.9             # Nucleus sampling
repetition_penalty=1.2 # Avoid repetition
```

---

## 🔧 Configuration

### Customizing the AI Model

Edit `rag_pipeline_enhanced.py`:

```python
# Use a larger model for better responses
llm_model="google/flan-t5-large"  # or "google/flan-t5-xl"

# Adjust chunk size
chunk_size=800  # Larger chunks = more context
chunk_overlap=150  # More overlap = better continuity
```

### Customizing the UI

Edit `frontend/tailwind.config.js` for colors:

```javascript
colors: {
  primary: {
    500: '#667eea',  // Main brand color
  },
}
```

---

## 📊 Performance Optimization

### For Better Speed
1. **Use GPU**: If available, PyTorch will automatically use CUDA
2. **Reduce top_k**: Fewer sources = faster responses
3. **Cache Results**: Implement Redis for repeated questions

### For Better Accuracy
1. **Increase top_k**: More sources = more comprehensive answers
2. **Use Larger Model**: `flan-t5-large` or `flan-t5-xl`
3. **Add More Documents**: More PDFs = broader knowledge

---

## 🌍 Deployment

### Option 1: Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy `app_enhanced.py`

### Option 2: Vercel (Frontend) + Railway (Backend)

**Frontend (Vercel):**
```bash
cd frontend
vercel deploy
```

**Backend (Railway):**
1. Create `Procfile`:
```
web: uvicorn backend.api:app --host 0.0.0.0 --port $PORT
```
2. Push to GitHub
3. Deploy on [Railway.app](https://railway.app)

### Option 3: Docker

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
```

---

## 🐛 Troubleshooting

### Common Issues

**1. TensorFlow Errors**
```bash
# Solution: Already handled in code
os.environ['TRANSFORMERS_NO_TF'] = '1'
```

**2. ChromaDB Permission Errors**
```bash
# Delete and recreate db folder
rm -rf db/
```

**3. Model Download Slow**
```bash
# Use a mirror
export HF_ENDPOINT=https://hf-mirror.com
```

**4. Out of Memory**
```bash
# Use smaller model
llm_model="google/flan-t5-small"
```

---

## 📚 Adding New Documents

1. Place PDF files in `data/` folder
2. Delete `db/` folder to force re-ingestion
3. Restart the application

**Supported Formats:**
- PDF (text-based, not scanned images)
- Must be in English or Hindi

---

## 🤝 Contributing

This is a social welfare project. Contributions welcome!

### Areas for Improvement
- [ ] Add more legal documents
- [ ] Support multiple languages
- [ ] Add voice input/output
- [ ] Implement user feedback system
- [ ] Add legal term glossary

---

## 📄 License

This project is open-source for educational and social welfare purposes.

**Disclaimer**: This tool provides general legal information only. It is not a substitute for professional legal advice. Always consult a qualified attorney for specific legal matters.

---

## 📞 Support

For issues or questions:
1. Check this guide
2. Review error logs
3. Check the [FastAPI docs](http://localhost:8000/docs) when backend is running

---

## 🎉 Success Criteria

Your setup is successful when:
- ✅ Streamlit app runs without errors
- ✅ Disclaimer is clearly visible (dark text on light background)
- ✅ Chat input clears after sending
- ✅ AI provides detailed, source-based answers
- ✅ Sources are displayed with page numbers
- ✅ UI is professional and accessible

---

**Built with ❤️ for social welfare and legal education**
