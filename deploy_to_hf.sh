#!/bin/bash

# HuggingFace Space Deployment Script
# This script copies all necessary files to your HF Space directory

echo "🚀 RAG Chatbot - HuggingFace Space Deployment"
echo "=============================================="
echo ""

# Check if HF space path is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide the path to your HF Space directory"
    echo ""
    echo "Usage: ./deploy_to_hf.sh <path-to-hf-space>"
    echo "Example: ./deploy_to_hf.sh ../rag-chatbot"
    echo ""
    echo "Steps to get your HF Space:"
    echo "1. Create Space at: https://huggingface.co/new-space"
    echo "2. Clone it: git clone https://huggingface.co/spaces/<username>/rag-chatbot"
    echo "3. Run this script with the cloned directory path"
    exit 1
fi

HF_SPACE_DIR="$1"

# Verify HF space directory exists
if [ ! -d "$HF_SPACE_DIR" ]; then
    echo "❌ Error: Directory not found: $HF_SPACE_DIR"
    exit 1
fi

# Verify it's a git repo
if [ ! -d "$HF_SPACE_DIR/.git" ]; then
    echo "⚠️  Warning: $HF_SPACE_DIR doesn't appear to be a git repository"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📂 Target directory: $HF_SPACE_DIR"
echo ""

# Copy essential files
echo "📋 Copying files..."

# Rename Dockerfile
if [ -f "Dockerfile.huggingface" ]; then
    cp Dockerfile.huggingface "$HF_SPACE_DIR/Dockerfile"
    echo "✅ Copied: Dockerfile.huggingface → Dockerfile"
else
    echo "❌ Missing: Dockerfile.huggingface"
    exit 1
fi

# Copy Python files
for file in requirements.txt config.py rag_chain.py main.py app.py .env.example; do
    if [ -f "$file" ]; then
        cp "$file" "$HF_SPACE_DIR/"
        echo "✅ Copied: $file"
    else
        echo "❌ Missing: $file"
        exit 1
    fi
done

# Create HF Space README
echo ""
echo "📝 Creating README.md for HuggingFace Space..."

cat > "$HF_SPACE_DIR/README.md" << 'EOF'
---
title: RAG Chatbot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# RAG Chatbot - AI-Powered Document Q&A

Upload documents (PDF, DOCX, TXT, MD) and ask questions - get intelligent answers with source citations!

## ✨ Features

- 📄 **Multi-format support** - PDF, DOCX, TXT, Markdown
- 💬 **Conversational memory** - Context-aware responses
- 🎯 **Source citations** - See exactly where answers come from
- 🚀 **Powered by Groq** - Fast Llama 3.3 70B inference
- 📊 **Vector search** - Pinecone for efficient retrieval
- 🔄 **Real-time** - Instant responses, no cold starts

## 🎮 How to Use

1. **📤 Upload** - Use the sidebar to upload your document
2. **💬 Ask** - Type questions about your document in the chat
3. **✅ Verify** - Click "View sources" to see citations

## 🛠️ Tech Stack

- **Backend**: FastAPI + LangChain
- **Frontend**: Streamlit
- **LLM**: Groq (Llama 3.3 70B)
- **Vector DB**: Pinecone
- **Embeddings**: HuggingFace all-MiniLM-L6-v2
- **Memory**: Redis

## 📁 Source Code

GitHub: https://github.com/YourUsername/RAG-Chatbot

---

Built with ❤️ using Claude Code
EOF

echo "✅ Created: README.md"

# List files in HF space
echo ""
echo "📦 Files in HF Space:"
ls -lah "$HF_SPACE_DIR" | grep -E '\.(py|txt|md)|Dockerfile'

echo ""
echo "✅ All files copied successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Add secrets in HF Space Settings:"
echo "   - GROQ_API_KEY"
echo "   - PINECONE_API_KEY"
echo "   - PINECONE_ENVIRONMENT"
echo "   - PINECONE_INDEX_NAME"
echo ""
echo "2. Commit and push to HF Space:"
echo "   cd $HF_SPACE_DIR"
echo "   git add ."
echo "   git commit -m \"Initial deployment: Complete RAG system\""
echo "   git push"
echo ""
echo "3. Wait for build (5-10 minutes)"
echo "4. Test your Space!"
echo ""
echo "🎉 Ready to deploy!"
