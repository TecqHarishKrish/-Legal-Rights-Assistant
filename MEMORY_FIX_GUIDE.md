# 🔧 Memory Fix Guide

## Problem
"The paging file is too small for this operation to complete" error occurs when loading AI models.

## Solution
I've fixed the issue by:

### 1. Using Smaller Model
- Changed from `google/flan-t5-base` (850MB) to `google/flan-t5-small` (150MB)
- Reduces memory usage by ~80%
- Still provides good quality answers

### 2. Disabled Web Search by Default
- Reduces memory overhead
- Can be enabled in settings if needed

### 3. Improved Text Sizing
- Fixed button text size in sidebar
- Improved message readability
- Better disclaimer text formatting

## How to Run

```bash
# Restart the application
streamlit run app_unified.py
```

The app should now load without memory errors!

## Additional Tips

### If Still Experiencing Issues:

1. **Close other applications** to free up RAM
2. **Increase virtual memory** in Windows:
   - Control Panel → System → Advanced System Settings
   - Performance → Settings → Advanced
   - Virtual Memory → Change
   - Set to "System managed size"

3. **Use even smaller settings** if needed:
   - Edit `app_unified.py`
   - Change `chunk_size` to 300-400
   - Reduce `top_k` to 1-2 sources

## Model Comparison

| Model | Size | RAM Usage | Quality |
|-------|------|-----------|---------|
| flan-t5-small | 150MB | Low | Good |
| flan-t5-base | 850MB | High | Very Good |
| flan-t5-large | 1.5GB | Very High | Excellent |

We're using **flan-t5-small** for optimal memory usage.

---

**The application should now work smoothly!** 🎉

