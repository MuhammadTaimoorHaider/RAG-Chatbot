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

## 🎮 How to Use

1. **📤 Upload** - Use the sidebar to upload your document
2. **💬 Ask** - Type questions about your document
3. **✅ Verify** - Click "View sources" to see citations

## 🛠️ Tech Stack

- **Backend**: FastAPI + LangChain
- **Frontend**: Streamlit
- **LLM**: Groq (Llama 3.3 70B)
- **Vector DB**: Pinecone
- **Embeddings**: HuggingFace all-MiniLM-L6-v2
- **Memory**: Redis
