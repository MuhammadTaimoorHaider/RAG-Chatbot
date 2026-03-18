"""
Configuration management using Pydantic Settings.
Loads environment variables from .env file and provides type-safe access.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Groq Configuration
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"

    # Embeddings Configuration (HuggingFace - local, no API key needed)
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Pinecone Configuration
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index_name: str = "production-rag-index"

    # Application Settings
    environment: str = "production"
    log_level: str = "INFO"
    max_upload_size_mb: int = 10
    allowed_file_types: str = "pdf,txt,md,docx"

    # Chunking Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # RAG Configuration
    top_k_results: int = 4
    max_conversation_history: int = 10

    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "*"

    # Streamlit Configuration
    streamlit_server_port: int = 8501
    api_base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create singleton instance
settings = Settings()
