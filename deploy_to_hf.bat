@echo off
REM HuggingFace Space Deployment Script for Windows
REM This script copies all necessary files to your HF Space directory

echo.
echo ========================================
echo RAG Chatbot - HuggingFace Deployment
echo ========================================
echo.

REM Check if HF space path is provided
if "%~1"=="" (
    echo ERROR: Please provide the path to your HF Space directory
    echo.
    echo Usage: deploy_to_hf.bat ^<path-to-hf-space^>
    echo Example: deploy_to_hf.bat ..\rag-chatbot
    echo.
    echo Steps to get your HF Space:
    echo 1. Create Space at: https://huggingface.co/new-space
    echo 2. Clone it: git clone https://huggingface.co/spaces/^<username^>/rag-chatbot
    echo 3. Run this script with the cloned directory path
    exit /b 1
)

set HF_SPACE_DIR=%~1

REM Verify HF space directory exists
if not exist "%HF_SPACE_DIR%" (
    echo ERROR: Directory not found: %HF_SPACE_DIR%
    exit /b 1
)

echo Target directory: %HF_SPACE_DIR%
echo.
echo Copying files...
echo.

REM Copy Dockerfile
if exist "Dockerfile.huggingface" (
    copy /Y "Dockerfile.huggingface" "%HF_SPACE_DIR%\Dockerfile" >nul
    echo [OK] Copied: Dockerfile.huggingface -^> Dockerfile
) else (
    echo [ERROR] Missing: Dockerfile.huggingface
    exit /b 1
)

REM Copy Python and config files
for %%f in (requirements.txt config.py rag_chain.py main.py app.py .env.example) do (
    if exist "%%f" (
        copy /Y "%%f" "%HF_SPACE_DIR%\" >nul
        echo [OK] Copied: %%f
    ) else (
        echo [ERROR] Missing: %%f
        exit /b 1
    )
)

REM Create HF Space README
echo.
echo Creating README.md for HuggingFace Space...
(
echo ---
echo title: RAG Chatbot
echo emoji: 🤖
echo colorFrom: blue
echo colorTo: green
echo sdk: docker
echo pinned: false
echo license: mit
echo ---
echo.
echo # RAG Chatbot - AI-Powered Document Q^&A
echo.
echo Upload documents ^(PDF, DOCX, TXT, MD^) and ask questions - get intelligent answers with source citations!
echo.
echo ## ✨ Features
echo.
echo - 📄 **Multi-format support** - PDF, DOCX, TXT, Markdown
echo - 💬 **Conversational memory** - Context-aware responses
echo - 🎯 **Source citations** - See exactly where answers come from
echo - 🚀 **Powered by Groq** - Fast Llama 3.3 70B inference
echo - 📊 **Vector search** - Pinecone for efficient retrieval
echo - 🔄 **Real-time** - Instant responses, no cold starts
echo.
echo ## 🎮 How to Use
echo.
echo 1. **📤 Upload** - Use the sidebar to upload your document
echo 2. **💬 Ask** - Type questions about your document in the chat
echo 3. **✅ Verify** - Click "View sources" to see citations
echo.
echo ## 🛠️ Tech Stack
echo.
echo - **Backend**: FastAPI + LangChain
echo - **Frontend**: Streamlit
echo - **LLM**: Groq ^(Llama 3.3 70B^)
echo - **Vector DB**: Pinecone
echo - **Embeddings**: HuggingFace all-MiniLM-L6-v2
echo - **Memory**: Redis
echo.
echo ## 📁 Source Code
echo.
echo GitHub: https://github.com/YourUsername/RAG-Chatbot
echo.
echo ---
echo.
echo Built with ❤️ using Claude Code
) > "%HF_SPACE_DIR%\README.md"

echo [OK] Created: README.md
echo.

REM List files
echo Files ready in HF Space:
dir /B "%HF_SPACE_DIR%\*.py" "%HF_SPACE_DIR%\*.txt" "%HF_SPACE_DIR%\*.md" "%HF_SPACE_DIR%\Dockerfile" 2>nul

echo.
echo ========================================
echo SUCCESS! All files copied
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Add secrets in HF Space Settings:
echo    - GROQ_API_KEY
echo    - PINECONE_API_KEY
echo    - PINECONE_ENVIRONMENT
echo    - PINECONE_INDEX_NAME
echo.
echo 2. Commit and push to HF Space:
echo    cd %HF_SPACE_DIR%
echo    git add .
echo    git commit -m "Initial deployment: Complete RAG system"
echo    git push
echo.
echo 3. Wait for build ^(5-10 minutes^)
echo 4. Test your Space!
echo.
echo Ready to deploy! 🚀
echo.
pause
