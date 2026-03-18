# RAG Chatbot - Production-Ready System

A production-ready Retrieval Augmented Generation (RAG) chatbot built with LangChain, Pinecone, OpenAI, FastAPI, and Streamlit. Upload documents and ask questions with conversational memory.

## Features

- **Multi-Format Document Support**: PDF, DOCX, TXT, and Markdown files
- **Conversational Memory**: Context-aware responses using conversation history
- **Vector Search**: Semantic similarity search with Pinecone
- **REST API**: FastAPI backend with comprehensive endpoints
- **User-Friendly UI**: Streamlit chat interface
- **Batch Ingestion**: CLI tool for bulk document processing
- **Production-Ready**: Docker containerization with health checks
- **Secure**: Environment-based configuration, no hardcoded secrets

## Architecture

```
┌─────────────────────────────────────────────┐
│     Streamlit UI (Port 8501)                │
│     - Chat Interface                        │
│     - Document Upload                       │
│     - Session Management                    │
└────────────────┬────────────────────────────┘
                 │ HTTP REST API
                 ▼
┌─────────────────────────────────────────────┐
│     FastAPI Backend (Port 8000)             │
│     - /chat (RAG queries)                   │
│     - /upload (Document processing)         │
│     - /health (System status)               │
│     - /history (Conversation management)    │
└────────────────┬────────────────────────────┘
                 │
        ┌────────┴─────────┐
        ▼                  ▼
┌─────────────┐    ┌──────────────┐
│  Pinecone   │    │    Redis     │
│  (Vectors)  │    │  (Memory)    │
└─────────────┘    └──────────────┘
        │
        ▼
┌─────────────┐
│   OpenAI    │
│ (LLM+Embed) │
└─────────────┘
```

## Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose** (for containerized deployment)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Pinecone API Key** ([Sign up here](https://www.pinecone.io/))
- **Redis** (included in Docker Compose, or local installation)

## Quick Start

### 1. Clone and Setup

```bash
# Clone or create project directory
cd RAG

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# Required: OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENVIRONMENT
```

### 2. Configure Environment Variables

Edit `.env` file:

```bash
# OpenAI
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Pinecone
PINECONE_API_KEY=your-pinecone-key-here
PINECONE_ENVIRONMENT=us-east1-gcp
PINECONE_INDEX_NAME=production-rag-index
```

### 3. Run with Docker (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Access applications:
# - Streamlit UI: http://localhost:8501
# - FastAPI Docs: http://localhost:8000/docs
# - Health Check: http://localhost:8000/health
```

### 4. Run Locally (Without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir logs uploads

# Start Redis (if not using Docker)
# On macOS: brew services start redis
# On Linux: sudo systemctl start redis
# On Windows: Install from https://redis.io/download

# Start FastAPI backend
python main.py
# Or: uvicorn main:app --reload --port 8000

# In a new terminal, start Streamlit
streamlit run app.py

# Access:
# - Streamlit: http://localhost:8501
# - API: http://localhost:8000
```

## Usage

### Web Interface (Streamlit)

1. **Access UI**: Open http://localhost:8501
2. **Upload Documents**: Use sidebar to upload PDF, DOCX, TXT, or MD files
3. **Ask Questions**: Type questions in the chat input
4. **View Sources**: Expand source citations to see relevant document excerpts
5. **Manage Sessions**: Clear chat or start new session from sidebar

### CLI Document Ingestion

Batch process documents using the command-line tool:

```bash
# Ingest single file
python ingest.py --file document.pdf

# Ingest entire directory
python ingest.py --directory ./docs

# Ingest recursively
python ingest.py --directory ./docs --recursive

# Specify namespace
python ingest.py --file report.docx --namespace project-alpha

# Ingest multiple files
python ingest.py --batch file1.pdf file2.txt file3.docx

# Verbose logging
python ingest.py --file document.pdf --verbose
```

### API Endpoints

#### POST /chat
Query the RAG system with conversation memory.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "session_id": "user-123",
    "namespace": "default"
  }'
```

#### POST /upload
Upload and process a document.

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf" \
  -F "namespace=default"
```

#### GET /health
Check system health status.

```bash
curl http://localhost:8000/health
```

#### GET /history/{session_id}
Retrieve conversation history.

```bash
curl http://localhost:8000/history/user-123
```

#### DELETE /history/{session_id}
Clear conversation history.

```bash
curl -X DELETE http://localhost:8000/history/user-123
```

## Project Structure

```
RAG/
├── config.py              # Pydantic settings management
├── rag_chain.py           # Core RAG logic (Document processing, embeddings, retrieval)
├── main.py                # FastAPI backend server
├── app.py                 # Streamlit frontend
├── ingest.py              # CLI batch ingestion tool
├── requirements.txt       # Python dependencies
├── Dockerfile             # API service container
├── Dockerfile.streamlit   # Streamlit service container
├── docker-compose.yml     # Multi-service orchestration
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore patterns
├── README.md              # This file
├── logs/                  # Application logs (auto-created)
└── uploads/               # Temporary upload storage (auto-created)
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `OPENAI_MODEL` | LLM model for chat | gpt-4-turbo-preview |
| `OPENAI_EMBEDDING_MODEL` | Embedding model | text-embedding-3-small |
| `PINECONE_API_KEY` | Pinecone API key (required) | - |
| `PINECONE_ENVIRONMENT` | Pinecone environment (required) | - |
| `PINECONE_INDEX_NAME` | Vector index name | production-rag-index |
| `CHUNK_SIZE` | Document chunk size | 1000 |
| `CHUNK_OVERLAP` | Chunk overlap size | 200 |
| `TOP_K_RESULTS` | Number of results to retrieve | 4 |
| `MAX_CONVERSATION_HISTORY` | Max messages in memory | 10 |
| `REDIS_HOST` | Redis hostname | localhost |
| `REDIS_PORT` | Redis port | 6379 |
| `API_PORT` | FastAPI port | 8000 |
| `CORS_ORIGINS` | CORS allowed origins | * |

### Chunking Strategy

- **Size**: 1000 characters (optimal for OpenAI embeddings)
- **Overlap**: 200 characters (maintains context across chunks)
- **Splitter**: RecursiveCharacterTextSplitter with semantic separators
- **Metadata**: Preserves filename, page number, chunk ID, timestamp

### Memory Management

- **Primary**: Redis with 1-hour TTL (production)
- **Fallback**: In-memory dictionary (local development)
- **Capacity**: Last 50 messages per session in Redis
- **Context**: Last 5 messages passed to LLM

## Deployment

### Docker Compose (Local/VPS)

```bash
# Production deployment
docker-compose up -d

# View logs
docker-compose logs -f api

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Remove volumes (clears Redis data)
docker-compose down -v
```

### Railway.app

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Deploy:
```bash
railway login
railway init
railway up
```

3. Add environment variables in Railway dashboard
4. Access deployed URL

### Render.com

1. Create new Web Service from GitHub
2. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables
4. Deploy

### AWS/GCP/Azure

1. Build Docker image:
```bash
docker build -t rag-chatbot .
```

2. Push to container registry (ECR/GCR/ACR)
3. Deploy to container service (ECS/Cloud Run/Container Apps)
4. Configure environment variables and networking

## Monitoring & Logging

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-03-18T10:00:00Z",
  "services": {
    "pinecone": "connected",
    "openai": "operational",
    "redis": "connected"
  },
  "version": "1.0.0"
}
```

### Logs

Application logs are stored in `logs/` directory:

- `api_YYYY-MM-DD.log` - FastAPI backend logs
- `ingest_YYYY-MM-DD.log` - Ingestion script logs

Log rotation: 500MB max size, 10 days retention

## Troubleshooting

### API Connection Issues

**Problem**: Streamlit can't connect to API

**Solution**:
```bash
# Check API is running
curl http://localhost:8000/health

# Check Docker network
docker-compose ps

# Verify API_BASE_URL in Streamlit
# For Docker: API_BASE_URL=http://api:8000
# For local: API_BASE_URL=http://localhost:8000
```

### Pinecone Index Issues

**Problem**: "Index not found" error

**Solution**:
```python
# Create index manually
python -c "from rag_chain import VectorStoreManager; vm = VectorStoreManager(); vm.create_index()"
```

### Redis Connection Failed

**Problem**: Redis unavailable warning

**Solution**:
- System automatically falls back to in-memory storage
- For production, ensure Redis is running:
```bash
# Docker
docker-compose up redis

# Local
redis-cli ping  # Should return PONG
```

### Document Upload Fails

**Problem**: Upload returns 400/500 error

**Solutions**:
- Check file size (max 10MB by default)
- Verify file type (PDF, DOCX, TXT, MD only)
- Check API logs: `docker-compose logs api`

### Out of Memory Errors

**Problem**: Container crashes with OOM

**Solutions**:
- Increase Docker memory limits
- Reduce `CHUNK_SIZE` in .env
- Process documents in smaller batches
- Reduce `MAX_CONVERSATION_HISTORY`

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# With coverage
pytest --cov=. tests/
```

### Code Structure

**rag_chain.py** (Core Logic):
- `DocumentProcessor`: Load and chunk documents
- `EmbeddingManager`: Generate OpenAI embeddings
- `VectorStoreManager`: Pinecone operations
- `ConversationManager`: Memory management
- `RAGChain`: Main orchestrator

**main.py** (API):
- FastAPI endpoints
- Request/response models
- Error handling
- Middleware configuration

**app.py** (Frontend):
- Streamlit chat interface
- File upload UI
- Session management
- API integration

**ingest.py** (CLI):
- Batch document processing
- Progress tracking
- Error handling
- Multi-format support

## Performance Optimization

### Recommended Settings

**Small dataset** (< 100 docs):
- `CHUNK_SIZE=1000`
- `TOP_K_RESULTS=4`
- Redis: 1GB memory

**Medium dataset** (100-1000 docs):
- `CHUNK_SIZE=800`
- `TOP_K_RESULTS=6`
- Redis: 2GB memory

**Large dataset** (> 1000 docs):
- `CHUNK_SIZE=600`
- `TOP_K_RESULTS=8`
- Redis: 4GB memory
- Consider Pinecone namespace partitioning

### Caching

Conversation memory is cached in Redis with 1-hour TTL. Frequently asked questions benefit from this caching.

## Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use environment-specific configurations** for production
3. **Rotate API keys regularly**
4. **Configure CORS** properly in production (not `*`)
5. **Use HTTPS** in production deployments
6. **Implement rate limiting** for public APIs
7. **Validate file uploads** (size, type, content)
8. **Run as non-root user** in containers (implemented)

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - feel free to use for personal or commercial projects.

## Support

For issues and questions:
- Check troubleshooting section above
- Review API docs: http://localhost:8000/docs
- Check logs: `docker-compose logs -f`

## Acknowledgments

Built with:
- [LangChain](https://langchain.com/) - RAG framework
- [Pinecone](https://www.pinecone.io/) - Vector database
- [OpenAI](https://openai.com/) - LLM and embeddings
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Streamlit](https://streamlit.io/) - UI framework
- [Redis](https://redis.io/) - Caching and memory

---

**Status**: Production-Ready ✅

**Version**: 1.0.0

**Last Updated**: March 2026
