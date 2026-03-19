"""
FastAPI backend for RAG Chatbot.
Provides REST API endpoints for chat, document upload, and history management.
"""

import os
import sys
import tempfile
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from loguru import logger

# Import RAG components
from rag_chain import (
    initialize_rag_system,
    DocumentProcessingError,
    VectorStoreError,
    LLMError
)
from config import settings


# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.log_level
)
logger.add(
    "logs/api_{time:YYYY-MM-DD}.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG"
)


# Pydantic Models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str = Field(..., min_length=1, description="User question")
    session_id: str = Field(..., min_length=1, description="Session identifier")
    namespace: str = Field(default="default", description="Document namespace")


class Source(BaseModel):
    """Source document information."""
    id: int
    content: str
    metadata: Dict[str, Any]
    filename: str
    page: int
    chunk_id: int


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str
    sources: List[Source]
    session_id: str
    metadata: Dict[str, Any]


class UploadResponse(BaseModel):
    """Response model for upload endpoint."""
    filename: str
    chunks_created: int
    status: str
    message: str
    metadata: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: str
    services: Dict[str, str]
    version: str


class HistoryResponse(BaseModel):
    """Response model for conversation history."""
    session_id: str
    messages: List[Dict[str, Any]]
    message_count: int


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str
    code: str


# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Production RAG chatbot with conversation memory",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global RAG system components
rag_system = None


@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup."""
    global rag_system
    try:
        logger.info("Starting RAG Chatbot API...")
        os.makedirs("logs", exist_ok=True)
        os.makedirs("uploads", exist_ok=True)

        rag_system = initialize_rag_system()
        logger.info("RAG system initialized successfully")
        logger.info(f"API running on {settings.api_host}:{settings.api_port}")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {str(e)}")
        raise RuntimeError(f"Startup failed: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down RAG Chatbot API...")


# Error Handlers
@app.exception_handler(DocumentProcessingError)
async def document_processing_error_handler(request, exc):
    logger.error(f"Document processing error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Document Processing Error",
            "message": str(exc),
            "code": "DOCUMENT_PROCESSING_ERROR"
        }
    )


@app.exception_handler(VectorStoreError)
async def vector_store_error_handler(request, exc):
    logger.error(f"Vector store error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Vector Store Error",
            "message": str(exc),
            "code": "VECTOR_STORE_ERROR"
        }
    )


@app.exception_handler(LLMError)
async def llm_error_handler(request, exc):
    logger.error(f"LLM error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "LLM Error",
            "message": str(exc),
            "code": "LLM_ERROR"
        }
    )


# API Endpoints

@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint."""
    return {
        "message": "RAG Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Chat endpoint with RAG and conversation memory.

    - **question**: User's question
    - **session_id**: Unique session identifier for conversation context
    - **namespace**: Document namespace (default: "default")

    Returns answer with source citations and metadata.
    """
    try:
        logger.info(f"Chat request from session {request.session_id}: {request.question[:50]}...")

        if not rag_system:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="RAG system not initialized"
            )

        # Query RAG chain
        result = rag_system["rag_chain"].query(
            question=request.question,
            session_id=request.session_id,
            namespace=request.namespace
        )

        logger.info(f"Chat response generated in {result['metadata']['total_time_ms']}ms")
        return result

    except LLMError as e:
        raise
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )


@app.post("/upload", response_model=UploadResponse, tags=["Documents"])
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload"),
    namespace: str = Form(default="default", description="Document namespace")
):
    """
    Upload and process a document.

    Supports: PDF, DOCX, TXT, MD files.
    Maximum size: 10MB (configurable).

    - **file**: Document file
    - **namespace**: Namespace for document organization

    Returns processing status and chunk count.
    """
    try:
        logger.info(f"Upload request: {file.filename} (namespace: {namespace})")

        if not rag_system:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="RAG system not initialized"
            )

        # Validate file type
        file_extension = Path(file.filename).suffix.lstrip('.').lower()
        allowed_types = settings.allowed_file_types.split(',')

        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file_extension}. Allowed: {allowed_types}"
            )

        # Validate file size
        file_content = await file.read()
        file_size_mb = len(file_content) / (1024 * 1024)

        if file_size_mb > settings.max_upload_size_mb:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large: {file_size_mb:.2f}MB. Max: {settings.max_upload_size_mb}MB"
            )

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        try:
            # Load document
            document_processor = rag_system["document_processor"]

            if file_extension == 'pdf':
                documents = document_processor.load_pdf(temp_file_path)
            elif file_extension == 'docx':
                documents = document_processor.load_docx(temp_file_path)
            elif file_extension in ['txt', 'md']:
                documents = document_processor.load_text(temp_file_path)
            else:
                raise DocumentProcessingError(f"Unsupported file type: {file_extension}")

            # Chunk documents
            chunks = document_processor.chunk_documents(documents)

            # Upload to Pinecone
            result = rag_system["vector_store_manager"].upsert_documents(
                chunks,
                rag_system["embedding_manager"],
                namespace=namespace
            )

            logger.info(f"Uploaded {file.filename}: {len(chunks)} chunks created")

            return UploadResponse(
                filename=file.filename,
                chunks_created=len(chunks),
                status="success",
                message=f"Document uploaded and processed successfully",
                metadata={
                    "file_size_mb": round(file_size_mb, 2),
                    "pages": len(documents),
                    "processing_time_s": round(result["elapsed_time"], 2),
                    "namespace": namespace
                }
            )

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    except DocumentProcessingError as e:
        raise
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload processing failed: {str(e)}"
        )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Tests connectivity to:
    - Pinecone vector database
    - Groq API (via embeddings test)
    - Redis (if available)

    Returns service status and connectivity information.
    """
    try:
        services = {}

        # Check Pinecone
        try:
            if rag_system:
                pc = rag_system["vector_store_manager"].pc
                indexes = [index.name for index in pc.list_indexes()]
                services["pinecone"] = "connected" if indexes else "error"
            else:
                services["pinecone"] = "not_initialized"
        except Exception as e:
            logger.error(f"Pinecone health check failed: {str(e)}")
            services["pinecone"] = "error"

        # Check Embeddings (HuggingFace)
        try:
            if rag_system:
                # Simple embedding test
                test_embedding = rag_system["embedding_manager"].embed_query("test")
                services["embeddings"] = "operational" if len(test_embedding) > 0 else "error"
            else:
                services["embeddings"] = "not_initialized"
        except Exception as e:
            logger.error(f"Embeddings health check failed: {str(e)}")
            services["embeddings"] = "error"

        # Check Redis
        try:
            if rag_system:
                redis_available = rag_system["conversation_manager"].redis_available
                services["redis"] = "connected" if redis_available else "fallback_memory"
            else:
                services["redis"] = "not_initialized"
        except Exception as e:
            logger.error(f"Redis health check failed: {str(e)}")
            services["redis"] = "error"

        # Overall status
        has_errors = any(status == "error" for status in services.values())
        overall_status = "degraded" if has_errors else "healthy"

        return HealthResponse(
            status=overall_status,
            timestamp=datetime.utcnow().isoformat(),
            services=services,
            version="1.0.0"
        )

    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return HealthResponse(
            status="error",
            timestamp=datetime.utcnow().isoformat(),
            services={"error": str(e)},
            version="1.0.0"
        )


@app.get("/history/{session_id}", response_model=HistoryResponse, tags=["History"])
async def get_conversation_history(session_id: str, limit: int = 10):
    """
    Retrieve conversation history for a session.

    - **session_id**: Session identifier
    - **limit**: Maximum number of messages to retrieve (default: 10)

    Returns list of messages with timestamps.
    """
    try:
        if not rag_system:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="RAG system not initialized"
            )

        history = rag_system["conversation_manager"].get_history(session_id, limit=limit)

        return HistoryResponse(
            session_id=session_id,
            messages=history,
            message_count=len(history)
        )

    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve history: {str(e)}"
        )


@app.delete("/history/{session_id}", tags=["History"])
async def clear_conversation_history(session_id: str):
    """
    Clear conversation history for a session.

    - **session_id**: Session identifier

    Returns success status.
    """
    try:
        if not rag_system:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="RAG system not initialized"
            )

        rag_system["conversation_manager"].clear_history(session_id)

        logger.info(f"Cleared history for session: {session_id}")

        return {
            "status": "success",
            "message": f"Conversation history cleared for session {session_id}",
            "session_id": session_id
        }

    except Exception as e:
        logger.error(f"History clearing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear history: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True if settings.environment == "development" else False,
        log_level=settings.log_level.lower()
    )
