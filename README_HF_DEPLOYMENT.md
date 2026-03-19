# 🚀 Deploy to Hugging Face Spaces - Quick Guide

## ⚡ 5-Step Deployment (20 minutes total)

### Step 1: Create Hugging Face Space (3 min)
1. Go to: https://huggingface.co/new-space
2. Fill in:
   - **Space name**: `rag-chatbot` (or your choice)
   - **SDK**: Select "Docker"
   - **Hardware**: CPU basic - Free
   - **Visibility**: Public
3. Click **Create Space**

### Step 2: Add Secrets to Space (5 min)
In your new Space, click **Settings** → **Variables and secrets** → **New secret**

**Required secrets** (get these from your API providers):
```
GROQ_API_KEY = gsk_your-actual-groq-key-here
PINECONE_API_KEY = your-pinecone-api-key
PINECONE_ENVIRONMENT = us-east-1
PINECONE_INDEX_NAME = production-rag-index
```

**Optional** (defaults work fine):
```
GROQ_MODEL = llama-3.3-70b-versatile
EMBEDDING_MODEL = sentence-transformers/all-MiniLM-L6-v2
REDIS_HOST = localhost
REDIS_PORT = 6379
```

### Step 3: Clone Your Space Locally (2 min)
```bash
# Clone the empty HF Space
git clone https://huggingface.co/spaces/<YOUR-USERNAME>/rag-chatbot
cd rag-chatbot

# Verify you're in the right directory
pwd
```

### Step 4: Copy Project Files (3 min)
From your RAG project directory, copy files to the HF Space:

```bash
# Copy from RAG project to HF Space
cp ../Dockerfile.huggingface ./Dockerfile
cp ../requirements.txt .
cp ../config.py .
cp ../rag_chain.py .
cp ../main.py .
cp ../app.py .
cp ../.env.example .

# Verify files copied
ls -la
```

### Step 5: Create Space README & Deploy (7 min)
Create the Space metadata file:

```bash
cat > README.md << 'EOF'
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
```

**Now deploy:**
```bash
git add .
git commit -m "Initial deployment: Complete RAG system with Docker"
git push
```

### Step 6: Wait for Build & Test (5-10 min)
1. Go to your Space URL: `https://huggingface.co/spaces/<YOUR-USERNAME>/rag-chatbot`
2. Watch the **Logs** tab - build takes 5-10 minutes first time
3. Wait for **"Running"** status
4. Test the app:
   - Wait 30-60 seconds for services to start
   - Check "System Status" shows services connected
   - Upload a test document
   - Ask a question

---

## 🎯 What Gets Deployed

Your HF Space will run:
```
┌─────────────────────────────────────┐
│  Hugging Face Docker Space          │
│                                     │
│  Port 6379: Redis (memory)          │
│       ↓                            │
│  Port 8000: FastAPI (backend)       │
│       ↓                            │
│  Port 7860: Streamlit (frontend)    │
│       ↓                            │
│  Public: https://huggingface.co/... │
└─────────────────────────────────────┘
```

External services (via API):
- Groq API (LLM inference)
- Pinecone (vector storage)

---

## 🆘 Troubleshooting

### Build Failed
- Check **Logs** tab in your Space
- Common fix: Ensure all files copied correctly
- Verify `Dockerfile` exists (not `Dockerfile.huggingface`)

### App Shows "Application Error"
1. Check Space logs for Python errors
2. Verify all secrets are set in Settings
3. Ensure Pinecone index exists and matches `PINECONE_INDEX_NAME`
4. Verify Groq API key is valid

### "API Offline" in Streamlit
- Wait 1-2 minutes after "Running" status
- Redis and FastAPI need time to start
- Check logs for startup errors

### No Sources Returned
- Make sure you uploaded a document first
- Check that namespace matches (default: "default")
- Verify Pinecone index has vectors

---

## 📊 Files You Need in HF Space

```
rag-chatbot/           (HF Space root)
├── Dockerfile         ✅ (renamed from Dockerfile.huggingface)
├── README.md          ✅ (Space metadata + description)
├── requirements.txt   ✅
├── config.py          ✅
├── rag_chain.py       ✅
├── main.py            ✅
├── app.py             ✅
└── .env.example       ✅
```

**Don't upload:**
- ❌ .env (use HF Secrets instead!)
- ❌ .venv/ folders
- ❌ __pycache__/
- ❌ Old Dockerfiles

---

## ✨ After Deployment

### Update GitHub README
Add live demo link:
```markdown
## 🚀 Live Demo

**Try it now:** https://huggingface.co/spaces/<YOUR-USERNAME>/rag-chatbot

Upload a document and start asking questions!
```

### Share on LinkedIn
Template:
```
🚀 Just deployed my RAG Chatbot on Hugging Face Spaces!

Built a production-ready AI system that:
✅ Answers questions from your documents
✅ Provides source citations
✅ Maintains conversation context
✅ Runs 100% FREE on Hugging Face

Tech stack:
• FastAPI + LangChain
• Groq (Llama 3.3 70B)
• Pinecone vector search
• Streamlit UI
• Docker deployment

🔗 Live Demo: https://huggingface.co/spaces/<YOUR-USERNAME>/rag-chatbot
🔗 GitHub: https://github.com/YourUsername/RAG-Chatbot

#AI #MachineLearning #RAG #Python #Docker #LangChain
```

---

## 🎉 Success Checklist

- [ ] HF Space created
- [ ] All secrets added
- [ ] Files copied to Space
- [ ] Dockerfile renamed correctly
- [ ] README.md created with metadata
- [ ] Git pushed to Space
- [ ] Build completed successfully
- [ ] App shows "Running" status
- [ ] System status shows services connected
- [ ] Document upload works
- [ ] Chat works with sources
- [ ] Live URL shared on LinkedIn

---

## 💡 Why This Deployment is Perfect

✅ **$0/month forever**
✅ **Single URL** - easy to share
✅ **No cold starts** - always ready
✅ **Professional portfolio piece**
✅ **Zero maintenance** required
✅ **ML/AI community visibility**

---

**Ready to deploy?** Just follow the 5 steps above! 🚀
