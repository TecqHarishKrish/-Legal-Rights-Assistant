@echo off
echo ========================================
echo AI Legal Rights Assistant - Unified
echo ========================================
echo.
echo Starting enhanced AI assistant with:
echo - RAG-based document retrieval
echo - Web search integration
echo - Conversation history
echo - Export features
echo.

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)

REM Install dependencies
echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Starting application...
streamlit run app_unified.py

pause

