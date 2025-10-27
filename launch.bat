@echo off
echo ========================================
echo AI Legal Aid Chatbot - Launcher
echo ========================================
echo.
echo Choose your interface:
echo.
echo 1. Streamlit (Improved Chat Interface)
echo 2. Gradio (Alternative Interface)
echo 3. Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto streamlit
if "%choice%"=="2" goto gradio
if "%choice%"=="3" goto end
goto invalid

:streamlit
echo.
echo Starting Streamlit interface...
echo The app will open at http://localhost:8501
echo.
streamlit run app_v2.py
goto end

:gradio
echo.
echo Starting Gradio interface...
echo The app will open at http://localhost:7860
echo.
python app_gradio.py
goto end

:invalid
echo.
echo Invalid choice! Please run the script again.
pause
goto end

:end
