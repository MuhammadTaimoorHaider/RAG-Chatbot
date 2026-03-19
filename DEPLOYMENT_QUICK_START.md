# 🚀 Quick Deploy to Hugging Face Spaces + Render

**Time to Deploy: ~30 minutes**
**Cost: $0/month forever**

---

## Part 1: Setup Free Services (5 minutes)

### 1.1 Get Groq API Key (FREE - No Credit Card!)
```
1. Go to: https://console.groq.com/
2. Sign up with Google/GitHub
3. Click "Create API Key"
4. Copy the key (starts with gsk_)
```

### 1.2 Get Pinecone API Key (FREE)
```
1. Go to: https://www.pinecone.io/
2. Sign up
3. Create new index:
   - Name: production-rag-index
   - Dimensions: 384 (for all-MiniLM-L6-v2 model)
   - Metric: cosine
   - Environment: gcp-starter (free tier)
4. Copy API key and environment
```

### 1.3 Create Upstash Redis (FREE)
```
1. Go to: https://upstash.com/
2. Sign up (no credit card required)
3. Create Redis database
4. Copy: Host, Port, Password
```

---

## Part 2: Deploy Backend on Render (10 minutes)

### 2.1 Connect GitHub Repository
```
1. Go to: https://render.com/
2. Sign up with GitHub
3. New + → Web Service
4. Connect your repository: MuhammadTaimoorHaider/RAG-Chatbot
```

### 2.2 Configure Service
```
Name: rag-chatbot-api
Environment: Python
Branch: main
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Plan: Free
```

### 2.3 Set Environment Variables

Click "Advanced" → "Add Environment Variable", add each:

```bash
GROQ_API_KEY=gsk_your-key-here
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=gcp-starter
PINECONE_INDEX_NAME=production-rag-index

REDIS_HOST=your-host.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=your-upstash-password
REDIS_DB=0

ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=*
TOP_K_RESULTS=4
MAX_CONVERSATION_HISTORY=10
```

### 2.4 Deploy and Test
```bash
# Click "Deploy"
# Wait 3-5 minutes for build
# Copy your API URL: https://rag-chatbot-api-xxxx.onrender.com

# Test it:
curl https://your-api-url.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "pinecone": "connected",
    "embeddings": "operational",
    "redis": "connected"
  }
}
```

---

## Part 3: Deploy Frontend on Hugging Face (15 minutes)

### 3.1 Create HF Space

```
1. Go to: https://huggingface.co/new-space
2. Space name: rag-chatbot-demo
3. License: MIT
4. Select SDK: Streamlit
5. Hardware: CPU basic - Free (always on!)
6. Public or Private: Public (for portfolio)
7. Click "Create Space"
```

### 3.2 Upload Files to Space

**Option A: Using HF Web Interface**
```
1. In your Space, click "Files" tab
2. Click "Add file" → "Upload files"
3. Upload these files from your project:
   - app.py
   - requirements.txt
4. Click "Commit to main"
```

**Option B: Using Git (Recommended)**
```bash
# Clone your space
git clone https://huggingface.co/spaces/<your-username>/rag-chatbot-demo
cd rag-chatbot-demo

# Copy necessary files
cp /path/to/RAG/app.py .
cp /path/to/RAG/requirements.txt .

# Commit and push
git add .
git commit -m "Initial Streamlit deployment"
git push
```

### 3.3 Configure Space Secrets

In HF Space settings:
```
1. Click "Settings" tab
2. Scroll to "Variables and secrets"
3. Click "New secret"
4. Add:
   Name: API_BASE_URL
   Value: https://rag-chatbot-api-xxxx.onrender.com
5. Click "Save"
```

### 3.4 Verify Deployment

```
# Your app will build automatically (2-3 minutes)
# Access at: https://huggingface.co/spaces/<your-username>/rag-chatbot-demo

# Test:
1. Wait for build to complete
2. Upload a simple .txt file
3. Ask a question
4. Verify response with sources
```

---

## Part 4: Final Polish for LinkedIn (10 minutes)

### 4.1 Update Your GitHub README

Add live links to your README.md:
```markdown
## 🎥 Demo

**🔗 Live Demo:** https://huggingface.co/spaces/<your-username>/rag-chatbot-demo
**🔗 API Docs:** https://rag-chatbot-api-xxxx.onrender.com/docs
**🔗 GitHub:** https://github.com/MuhammadTaimoorHaider/RAG-Chatbot
```

### 4.2 Record Demo GIF

**Using ShareX (Windows) or Kap (Mac):**
```
1. Start recording
2. Open your HF Space
3. Upload a sample PDF (5-10 pages)
4. Ask: "What is the main topic of this document?"
5. Show the response with source citations
6. Stop recording (15-20 seconds max)
7. Save as demo.gif
8. Upload to GitHub repo
```

**Or use online tool:**
- https://www.screentogif.com/ (Windows)
- https://getkap.co/ (Mac)

### 4.3 Take Screenshots

Capture these 3 screens:
1. Main chat interface (empty state)
2. Document upload + question + response
3. Health monitoring (API /health endpoint)

Save as: `screenshots/` folder in your repo

---

## Part 5: LinkedIn Post

**Copy-Paste Ready:**

```
🚀 Just deployed my production-ready RAG Chatbot - 100% FREE to run!

💡 What it does:
Upload documents (PDF/DOCX/TXT) and ask questions - get AI-powered answers with source citations and conversational memory.

🛠️ Tech Stack:
• Backend: FastAPI + LangChain
• Frontend: Streamlit
• LLM: Groq (Llama 3.3 - FREE API, no credit card!)
• Vector DB: Pinecone
• Embeddings: HuggingFace (local, free)
• Memory: Redis (Upstash free tier)

✨ Key Features:
✅ Multi-format document support (PDF, DOCX, TXT, MD)
✅ Conversational context awareness
✅ Source-cited responses (no hallucinations)
✅ RESTful API with full documentation
✅ Docker containerized for easy deployment
✅ 100% free to run and host!

🔗 Live Demo: [Your HF Spaces URL]
🔗 GitHub: https://github.com/MuhammadTaimoorHaider/RAG-Chatbot
🔗 API Docs: [Your Render URL]/docs

[Attach demo GIF here]

Built this to learn production ML engineering - from RAG architecture to cloud deployment. Happy to discuss the technical details!

#MachineLearning #AI #RAG #Python #LangChain #FastAPI #Streamlit #GenerativeAI #OpenSource #MLOps #Portfolio

---

👉 Tag relevant people/companies
👉 Add 3-5 relevant hashtags
👉 Post during business hours (9 AM - 12 PM on weekdays)
```

---

## Troubleshooting

### Backend Sleeping on Render
**Problem**: First request takes 30 seconds
**Solution**:
- This is normal for free tier
- Consider upgrading to $7/month for always-on
- Or use a cron job to ping every 10 minutes (keep-alive)

### HF Space Build Failed
**Problem**: Requirements installation fails
**Solution**:
```bash
# Common issues:
# 1. Check requirements.txt versions
# 2. Remove torch dependencies if not needed on frontend
# 3. Check HF Space logs for specific error
```

### CORS Errors
**Problem**: Frontend can't connect to backend
**Solution**:
```bash
# In Render, add env var:
CORS_ORIGINS=https://huggingface.co

# Or for development:
CORS_ORIGINS=*
```

### Redis Connection Failed
**Problem**: Can't connect to Upstash
**Solution**:
- Verify host format: `xxx.upstash.io` (no https://)
- Port should be 6379 (or 6380 for TLS)
- Check password is copied correctly
- System falls back to in-memory if Redis fails (working but not persistent)

---

## Cost Breakdown (Monthly)

### Recommended Setup:
```
Groq API (LLM):              $0/month (free forever)
HuggingFace Embeddings:      $0/month (runs locally)
Pinecone (Vector DB):        $0/month (free tier, 1 index)
Upstash Redis:               $0/month (10k commands/day free)
Render Backend:              $0/month (free tier, sleeps after 15min)
HF Spaces Frontend:          $0/month (free forever, always on)
-------------------------------------------
Total:                       $0/month
```

### Optional Upgrades:
```
Render Always-On (no sleep):     +$7/month
More Render services:            +$7/month each
Pinecone additional indexes:     +$0 (need paid plan)
Domain name:                     +$12/year (~$1/month)
```

---

## What to Do After Deployment

1. ✅ Test thoroughly (upload docs, ask questions, check sources)
2. ✅ Monitor logs for errors
3. ✅ Add live URLs to your resume
4. ✅ Create demo video/GIF
5. ✅ Post on LinkedIn with screenshots
6. ✅ Add to portfolio website
7. ✅ Share in relevant communities (r/MachineLearning, HN)
8. ✅ Keep improving based on feedback

---

## Next Steps

Ready to deploy? Run:
```bash
# Test locally first
python main.py
# In another terminal:
streamlit run app.py

# If working, push to GitHub and follow deployment steps above
```

Good luck! 🚀
