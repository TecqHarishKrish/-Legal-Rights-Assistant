# 🚀 AI Legal Aid Chatbot - Launch Guide

## ✨ **NEW: Multiple Interface Options!**

Your chatbot now has **3 different interfaces** to choose from:

---

## 🎨 **Interface Options**

### 1️⃣ **Streamlit V2 (Recommended)** - Modern Chat Interface

**Features:**
- ✅ Beautiful gradient design
- ✅ Real chat bubbles (user & bot messages)
- ✅ Source cards with expandable details
- ✅ Smooth animations
- ✅ Better error handling
- ✅ Session-based chat history

**Launch:**
```bash
streamlit run app_v2.py
```

**URL:** http://localhost:8501

---

### 2️⃣ **Gradio** - Clean & Simple Interface

**Features:**
- ✅ Clean, minimalist design
- ✅ Built-in chat history
- ✅ Example questions
- ✅ Easy to use
- ✅ Mobile-friendly

**Launch:**
```bash
python app_gradio.py
```

**URL:** http://localhost:7860

---

### 3️⃣ **Original Streamlit** - Classic Interface

**Features:**
- ✅ Original design
- ✅ Detailed documentation
- ✅ Comprehensive sidebar

**Launch:**
```bash
streamlit run app.py
```

**URL:** http://localhost:8501

---

## 🎯 **Quick Start (Windows)**

### **Option 1: Use the Launcher**
```bash
# Double-click or run:
launch.bat

# Then choose:
# 1 = Streamlit V2 (Recommended)
# 2 = Gradio
```

### **Option 2: Direct Launch**
```bash
# Streamlit V2 (Recommended)
streamlit run app_v2.py

# OR Gradio
python app_gradio.py
```

---

## 📊 **Comparison**

| Feature | Streamlit V2 | Gradio | Original |
|---------|-------------|--------|----------|
| **Design** | Modern, Gradient | Clean, Simple | Classic |
| **Chat Bubbles** | ✅ Yes | ✅ Yes | ❌ No |
| **Chat History** | ✅ Yes | ✅ Yes | ❌ No |
| **Error Handling** | ✅ Excellent | ✅ Good | ⚠️ Basic |
| **Mobile Friendly** | ✅ Yes | ✅ Yes | ⚠️ Partial |
| **Load Time** | Fast | Fast | Slow |
| **Animations** | ✅ Yes | ⚠️ Basic | ❌ No |

---

## 🎨 **What's New in V2?**

### **Streamlit V2 Improvements:**

1. **Chat Interface**
   - Real chat bubbles (purple for user, white for bot)
   - Message history persists during session
   - Smooth scrolling

2. **Better Error Handling**
   - Graceful error messages
   - Detailed error logs
   - System status indicators

3. **Enhanced UI**
   - Gradient headers
   - Modern color scheme
   - Improved spacing
   - Better mobile support

4. **Performance**
   - Faster initialization
   - Better caching
   - Reduced reloads

### **Gradio Features:**

1. **Simple & Clean**
   - Minimalist design
   - Easy navigation
   - Built-in examples

2. **Chat History**
   - Automatic message tracking
   - Clear conversation flow

3. **Mobile Optimized**
   - Responsive design
   - Touch-friendly

---

## 🐛 **Troubleshooting**

### **If Streamlit V2 doesn't start:**
```bash
# Stop any running instances
taskkill /F /IM streamlit.exe

# Start fresh
streamlit run app_v2.py
```

### **If Gradio doesn't start:**
```bash
# Install Gradio
pip install gradio --user

# Run
python app_gradio.py
```

### **Port already in use:**
```bash
# Streamlit on different port
streamlit run app_v2.py --server.port 8502

# Gradio on different port
# Edit app_gradio.py and change server_port
```

---

## 💡 **Recommended Workflow**

### **For Best Experience:**

1. **First Time:**
   - Use **Streamlit V2** for the best visual experience
   - Wait for PDF ingestion (2-5 minutes)

2. **Daily Use:**
   - **Streamlit V2** for desktop
   - **Gradio** for mobile or simple interface

3. **Troubleshooting:**
   - Try **Gradio** if Streamlit has issues
   - Check **Original** for detailed logs

---

## 🎯 **Example Usage**

### **Streamlit V2:**
1. Launch: `streamlit run app_v2.py`
2. Wait for "System ready!" message
3. Type question in input box
4. Click "🚀 Send"
5. View answer with sources
6. Continue conversation

### **Gradio:**
1. Launch: `python app_gradio.py`
2. Wait for "System ready!" in status
3. Type in chat box
4. Press Enter or click Send
5. View response with sources
6. Chat history auto-saves

---

## 📱 **Mobile Access**

Both interfaces work on mobile!

### **Access from phone:**
1. Find your computer's IP address:
   ```bash
   ipconfig
   # Look for IPv4 Address
   ```

2. **Streamlit:** `http://YOUR_IP:8501`
3. **Gradio:** `http://YOUR_IP:7860`

---

## 🎨 **Customization**

### **Change Colors (Streamlit V2):**
Edit `app_v2.py`, find the CSS section:
```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# Change to your preferred gradient
```

### **Change Theme (Gradio):**
Edit `app_gradio.py`:
```python
theme=gr.themes.Soft(
    primary_hue="blue",  # Change this
    secondary_hue="purple"  # And this
)
```

---

## 🚀 **Performance Tips**

### **For Faster Loading:**
1. Use **Gradio** (lighter weight)
2. Reduce number of sources (1-2)
3. Close other applications

### **For Better Quality:**
1. Use **Streamlit V2** (more features)
2. Increase sources (4-5)
3. Wait for complete responses

---

## 📞 **Need Help?**

### **Interface Issues:**
- Try different interface (Streamlit ↔ Gradio)
- Check browser console (F12)
- Clear browser cache

### **Model Issues:**
- Check terminal for errors
- Verify PDFs in `data/` folder
- Try restarting system

### **Performance Issues:**
- Close other apps
- Use Gradio (lighter)
- Reduce sources

---

## 🎉 **You're All Set!**

**Recommended: Start with Streamlit V2**

```bash
streamlit run app_v2.py
```

Then explore Gradio for a different experience!

**Happy Legal Research! ⚖️**

---

*Built with ❤️ using Streamlit, Gradio, HuggingFace & ChromaDB*
