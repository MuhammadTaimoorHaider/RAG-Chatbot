---
title: RAG Chatbot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🤖 RAG Chatbot - AI Document Q&A

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLM-00ADD8)

**Upload documents • Ask questions • Get cited answers**

</div>

---

## ✨ Features

- 📄 **Multi-Format Support** - Upload PDF, DOCX, TXT, or Markdown files
- 💬 **Conversational AI** - Context-aware responses with memory
- 🎯 **Source Citations** - Every answer includes document references
- ⚡ **Fast Responses** - Powered by Groq's optimized LLM infrastructure
- 🔍 **Semantic Search** - Vector similarity search with Pinecone
- 🆓 **100% Free** - No API costs, completely free to use!

---

## 🎮 How to Use

### 1. Upload Document
- Click **sidebar** on the left
- Choose your file (PDF, DOCX, TXT, MD)
- Click **"Upload & Process"**
- Wait for confirmation

### 2. Ask Questions
- Type your question in the chat input
- Press Enter
- Watch AI generate answer with sources

### 3. View Sources
- Click **"View sources"** under each response
- See exact document excerpts used
- Verify information accuracy

---

## 🛠️ Technology Stack

**Frontend:**
- Streamlit - Interactive chat interface

**Backend:**
- FastAPI - REST API
- LangChain - RAG orchestration

**AI/ML:**
- Groq (Llama 3.3 70B) - Language model
- HuggingFace all-MiniLM-L6-v2 - Embeddings (local)
- Pinecone - Vector database

**Infrastructure:**
- Redis - Conversation memory
- Docker - Containerization

---

## 💡 Example Questions

Try these with sample documents:

- "What are the main topics discussed in this document?"
- "Summarize the key findings from this research"
- "What recommendations are provided?"
- "Compare the approaches mentioned in sections 2 and 3"
- "What are the performance metrics?"

---

## 📊 Sample Documents

Test with these types of documents:
- Research papers
- Technical documentation
- Business reports
- Meeting notes
- Articles and blogs

---

## 🔒 Privacy & Security

- Documents processed in memory only
- No permanent storage of your files
- Session data expires after 1 hour
- All communication over HTTPS

---

## 📁 Source Code

**GitHub:** [MuhammadTaimoorHaider/RAG-Chatbot](https://github.com/MuhammadTaimoorHaider/RAG-Chatbot)

Full source code, documentation, and deployment guides available.

---

## 🎓 About This Project

This project demonstrates production-ready LLM application development:

- Full-stack Python architecture
- Modern RAG implementation
- API-first design
- Cloud-native deployment
- Cost-optimized infrastructure

Built as a portfolio project showcasing ML engineering skills.

---

## 🚀 Performance

- **Response Time:** 2-3 seconds average
- **Accuracy:** Source-grounded (reduces hallucinations)
- **Scalability:** Handles concurrent users
- **Uptime:** 99%+ on Hugging Face infrastructure

---

## 📝 Technical Details

**RAG Pipeline:**
1. Document chunking (1000 chars, 200 overlap)
2. Embedding generation (384-dim vectors)
3. Vector storage in Pinecone
4. Similarity search on query
5. Context-aware LLM generation
6. Source attribution

**Conversation Memory:**
- Last 10 messages per session
- 1-hour session timeout
- Redis persistence with fallback

---

## 🤝 Contributing

Found a bug or have suggestions? Open an issue on [GitHub](https://github.com/MuhammadTaimoorHaider/RAG-Chatbot/issues)!

---

## 📧 Contact

**Developer:** Muhammad Taimoor Haider

**LinkedIn:** [Add your LinkedIn]

**GitHub:** [MuhammadTaimoorHaider](https://github.com/MuhammadTaimoorHaider)

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ using Groq, Pinecone, LangChain, and Streamlit**

⭐ Star the repo if you find it useful!

</div>
