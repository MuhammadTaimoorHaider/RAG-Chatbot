# Portfolio Deployment Guide (Render + Managed Redis)

This guide gives you a stable, recruiter-friendly deployment for your RAG chatbot.

## Target Architecture

- Frontend: Streamlit web service on Render
- Backend: FastAPI web service on Render
- Memory: Managed Redis (Upstash or Redis Cloud)
- Vector DB: Pinecone
- LLM: Groq

## 1) Push This Repository to GitHub

- Ensure this repository includes:
  - render.yaml
  - runtime.txt
  - latest app.py, main.py, rag_chain.py, config.py, requirements.txt

## 2) Create Managed Redis

Use either provider below and copy credentials.

### Upstash Redis

- Create a Redis database in Upstash.
- Copy:
  - Host
  - Port
  - Password

### Redis Cloud

- Create a free Redis database.
- Copy:
  - Host
  - Port
  - Password (if required)

## 3) Deploy on Render from Blueprint

- Open Render dashboard.
- New + -> Blueprint
- Select your GitHub repository.
- Render reads render.yaml and creates two services:
  - rag-api
  - rag-streamlit

## 4) Set Environment Variables in Render

### Service: rag-api

Set these values:

- GROQ_API_KEY = your Groq key
- GROQ_MODEL = llama-3.3-70b-versatile
- PINECONE_API_KEY = your Pinecone key
- PINECONE_ENVIRONMENT = your Pinecone region (example: us-east-1)
- PINECONE_INDEX_NAME = production-rag-index
- REDIS_HOST = from Redis provider
- REDIS_PORT = from Redis provider
- REDIS_PASSWORD = from Redis provider
- REDIS_DB = 0

Optional tuning:

- TOP_K_RESULTS = 4
- MAX_CONVERSATION_HISTORY = 10
- LOG_LEVEL = INFO

### Service: rag-streamlit

Set this value after rag-api is live:

- API_BASE_URL = https://<your-rag-api-service>.onrender.com

## 5) Verify Deployment

Backend checks:

- Open https://<your-rag-api-service>.onrender.com/health
- Confirm JSON shows:
  - status healthy
  - pinecone connected
  - redis connected

Frontend checks:

- Open Streamlit URL
- Upload a small TXT or MD file
- Ask one question
- Confirm response has sources

## 6) Portfolio Presentation Checklist

- Add Live Demo link (Streamlit URL)
- Add API Docs link: https://<api-url>/docs
- Add 20-40 second demo GIF:
  - upload document
  - ask question
  - show citations
- Add architecture image in README or portfolio page
- Add 4 impact bullets on what you built and fixed

## 7) Resume/Portfolio Description (Copy Ready)

Built a production-style Retrieval Augmented Generation chatbot with Streamlit frontend and FastAPI backend, using Pinecone for semantic search, Groq for LLM responses, and Redis for session memory. Implemented document ingestion (PDF, DOCX, TXT, MD), source-cited answers, health monitoring, and cloud deployment with managed services.

## 8) Optional: Hugging Face Space for Showcase

If you want a second public demo channel:

- Deploy only Streamlit UI on Hugging Face Spaces
- Keep backend API on Render
- Set API_BASE_URL in Space secrets to your Render API URL

This gives a polished portfolio presence while keeping backend reliability.
