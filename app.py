"""
Streamlit frontend for RAG Chatbot.
Provides user-friendly chat interface with document upload and conversation management.
"""

import os
import uuid
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

import streamlit as st
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DEFAULT_NAMESPACE = "default"


# Page Configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS
st.markdown("""
<style>
    :root {
        --chat-text: #e2e8f0;
        --user-bg: #1d4ed8;
        --assistant-bg: #1e293b;
        --chat-border: #334155;
        --panel-bg: #0f172a;
        --panel-border: #334155;
        --brand: #0ea5a4;
    }

    .stApp {
        background: radial-gradient(circle at top right, #111827 0%, #020617 42%, #0f172a 100%);
        color: #e2e8f0;
    }

    .stApp p,
    .stApp label,
    .stApp span,
    .stApp li,
    .stMarkdown,
    .stCaption {
        color: #cbd5e1;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
        border-right: 1px solid #1f2937;
    }

    [data-testid="stSidebar"] * {
        color: #cbd5e1;
    }

    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: #0f172a;
        color: #e2e8f0;
        border: 1px solid #334155;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea textarea::placeholder {
        color: #64748b;
    }

    .top-panel {
        background: linear-gradient(120deg, #0f172a 0%, #0f766e 100%);
        color: #ffffff;
        padding: 1.1rem 1.25rem;
        border-radius: 0.9rem;
        margin-bottom: 0.8rem;
        border: 1px solid #1f2937;
        box-shadow: 0 10px 30px rgba(2, 6, 23, 0.4);
    }

    .top-panel-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .top-panel-subtitle {
        font-size: 0.95rem;
        opacity: 0.96;
        margin-bottom: 0;
    }

    .metric-chip {
        background: var(--panel-bg);
        border: 1px solid var(--panel-border);
        border-radius: 0.8rem;
        padding: 0.65rem 0.8rem;
        margin: 0.2rem 0;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.78rem;
        margin-bottom: 0.1rem;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 1rem;
        font-weight: 700;
    }

    .main-header {
        font-size: 2.1rem;
        font-weight: bold;
        margin-bottom: 0.35rem;
    }

    .sub-header {
        color: #94a3b8;
        margin-bottom: 0.8rem;
        font-size: 1rem;
    }

    .chat-shell {
        background: #0b1220;
        border: 1px solid #1f2937;
        border-radius: 1rem;
        padding: 0.7rem 0.9rem;
        box-shadow: 0 8px 20px rgba(2, 6, 23, 0.35);
        min-height: 340px;
        margin-bottom: 0.8rem;
    }

    .assistant-meta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 0.5rem;
    }

    .meta-pill {
        border: 1px solid #134e4a;
        background: #0f2a2a;
        color: #5eead4;
        border-radius: 999px;
        padding: 0.18rem 0.55rem;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .empty-state {
        border: 1px dashed #334155;
        border-radius: 0.9rem;
        padding: 1.2rem;
        text-align: center;
        background: #0f172a;
        color: #cbd5e1;
        margin: 0.25rem 0.15rem 0.4rem;
    }

    .source-card {
        border: 1px solid #334155;
        background: #0f172a;
        border-radius: 0.7rem;
        padding: 0.65rem 0.75rem;
        margin-bottom: 0.55rem;
    }

    .source-title {
        color: #e2e8f0;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .source-snippet {
        color: #94a3b8;
        font-size: 0.82rem;
        line-height: 1.45;
    }

    .chat-hint {
        font-size: 0.82rem;
        color: #64748b;
        margin-top: 0.15rem;
    }

    .stButton > button {
        background: #134e4a;
        color: #ecfeff;
        border: 1px solid #0f766e;
    }

    .stButton > button:hover {
        background: #0f766e;
        color: #ffffff;
    }

    [data-testid="stChatInput"] {
        background: #0b1220;
        border: 1px solid #1f2937;
        border-radius: 0.75rem;
    }

    [data-testid="stChatMessage"] {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)


# Session State Initialization
def initialize_session():
    """Initialize session state variables."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "namespace" not in st.session_state:
        st.session_state.namespace = DEFAULT_NAMESPACE


# API Functions
def check_api_health() -> Dict[str, Any]:
    """Check API health status."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"status": "error", "error": str(e)}


def send_chat_message(question: str, session_id: str, namespace: str) -> Optional[Dict[str, Any]]:
    """Send chat message to API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "question": question,
                "session_id": session_id,
                "namespace": namespace
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Chat API error: {str(e)}")
        return None


def upload_document(file, namespace: str) -> Optional[Dict[str, Any]]:
    """Upload document to API."""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        data = {"namespace": namespace}

        response = requests.post(
            f"{API_BASE_URL}/upload",
            files=files,
            data=data,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Upload API error: {str(e)}")
        return None


def get_conversation_history(session_id: str) -> List[Dict[str, Any]]:
    """Get conversation history from API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/history/{session_id}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("messages", [])
    except Exception as e:
        st.error(f"History API error: {str(e)}")
        return []


def clear_conversation_history(session_id: str) -> bool:
    """Clear conversation history via API."""
    try:
        response = requests.delete(
            f"{API_BASE_URL}/history/{session_id}",
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Clear history API error: {str(e)}")
        return False


# UI Components
def display_chat_message(
    role: str,
    content: str,
    sources: Optional[List[Dict]] = None,
    timestamp: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
):
    """Display a chat message with optional sources."""
    icon = "🧑" if role == "user" else "🤖"
    pretty_time = ""
    if timestamp:
        try:
            pretty_time = datetime.fromisoformat(timestamp).strftime("%I:%M %p")
        except Exception:
            pretty_time = ""

    with st.chat_message(role, avatar=icon):
        st.markdown(content)
        if pretty_time:
            st.caption(pretty_time)

        if role == "assistant" and metadata:
            chips = []
            if metadata.get("model"):
                chips.append(f"<span class='meta-pill'>Model: {metadata['model']}</span>")
            if metadata.get("total_time_ms"):
                chips.append(f"<span class='meta-pill'>Latency: {metadata['total_time_ms']} ms</span>")
            if metadata.get("num_sources") is not None:
                chips.append(f"<span class='meta-pill'>Sources: {metadata['num_sources']}</span>")

            if chips:
                st.markdown(f"<div class='assistant-meta-row'>{''.join(chips)}</div>", unsafe_allow_html=True)

        # Display sources if available
        if sources and role == "assistant":
            with st.expander(f"📚 View {len(sources)} source(s)"):
                for i, source in enumerate(sources):
                    source_name = source.get("filename", "Unknown")
                    source_page = source.get("page", "N/A")
                    source_chunk = source.get("chunk_id", "N/A")
                    source_text = source.get("content", "")
                    source_text = source_text[:320] + "..." if len(source_text) > 320 else source_text

                    st.markdown(
                        f"""
                        <div class="source-card">
                            <div class="source-title">Source {i + 1}: {source_name} · p.{source_page} · chunk {source_chunk}</div>
                            <div class="source-snippet">{source_text}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


def render_sidebar():
    """Render sidebar with controls and information."""
    with st.sidebar:
        st.markdown("### 🤖 RAG Chatbot")
        st.divider()

        # API Health Status
        st.markdown("#### System Status")
        health = check_api_health()

        if health.get("status") == "healthy":
            st.success("✓ API Connected")
        elif health.get("status") == "degraded":
            st.warning("⚠ API Degraded")
        else:
            st.error("✗ API Offline")

        # Display service status
        if "services" in health:
            with st.expander("Service Details"):
                for service, status in health["services"].items():
                    if status in ["connected", "operational"]:
                        icon = "✓"
                        label = status
                    elif status in ["fallback_memory", "not_initialized"]:
                        icon = "⚠"
                        label = "using in-memory fallback" if status == "fallback_memory" else status
                    else:
                        icon = "✗"
                        label = status

                    st.text(f"{icon} {service}: {label}")

        st.divider()

        # Namespace Selector
        st.markdown("#### Document Namespace")
        namespace = st.text_input(
            "Namespace",
            value=st.session_state.namespace,
            help="Organize documents by project or category"
        )
        if namespace != st.session_state.namespace:
            st.session_state.namespace = namespace

        st.divider()

        # Document Upload
        st.markdown("#### Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "txt", "md", "docx"],
            help="Upload PDF, TXT, MD, or DOCX files"
        )

        if uploaded_file is not None:
            if st.button("📤 Upload & Process", use_container_width=True):
                with st.spinner("Processing document..."):
                    result = upload_document(uploaded_file, st.session_state.namespace)

                    if result and result.get("status") == "success":
                        st.success(f"✓ Uploaded {result['filename']}")
                        st.info(f"Created {result['chunks_created']} chunks")
                    else:
                        st.error("Upload failed")

        st.divider()

        # Conversation Management
        st.markdown("#### Conversation")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                if clear_conversation_history(st.session_state.session_id):
                    st.session_state.messages = []
                    st.success("Chat cleared")
                    st.rerun()

        with col2:
            if st.button("🔄 New Session", use_container_width=True):
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.messages = []
                st.success("New session started")
                st.rerun()

        st.divider()

        # Session Info
        st.markdown("#### Session Info")
        st.text(f"ID: {st.session_state.session_id[:8]}...")
        st.text(f"Messages: {len(st.session_state.messages)}")
        st.text(f"Namespace: {st.session_state.namespace}")


def render_chat_interface():
    """Render main chat interface."""
    health = check_api_health()
    api_state = health.get("status", "error").capitalize()

    st.markdown(
        """
        <div class="top-panel">
            <div class="top-panel-title">RAG Assistant</div>
            <p class="top-panel-subtitle">Upload documents, ask context-aware questions, and get cited answers in real time.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(
            f"""
            <div class="metric-chip">
                <div class="metric-label">Messages</div>
                <div class="metric-value">{len(st.session_state.messages)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f"""
            <div class="metric-chip">
                <div class="metric-label">Namespace</div>
                <div class="metric-value">{st.session_state.namespace}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_c:
        st.markdown(
            f"""
            <div class="metric-chip">
                <div class="metric-label">API Status</div>
                <div class="metric-value">{api_state}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="main-header">Chat Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional Q&A stream with citations and response metadata.</div>', unsafe_allow_html=True)

    st.divider()

    # Display chat history
    chat_container = st.container(border=False)

    with chat_container:
        st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

        if not st.session_state.messages:
            st.markdown(
                """
                <div class="empty-state">
                    <div><strong>No messages yet</strong></div>
                    <div class="chat-hint">Upload a document, then ask a specific question to start a professional chat session.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        for message in st.session_state.messages:
            display_chat_message(
                role=message["role"],
                content=message["content"],
                sources=message.get("sources"),
                timestamp=message.get("timestamp"),
                metadata=message.get("metadata"),
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })

        # Display user message immediately
        with chat_container:
            st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
            display_chat_message("user", prompt, timestamp=datetime.now().isoformat())
            st.markdown('</div>', unsafe_allow_html=True)

        # Get response from API
        with st.spinner("Thinking..."):
            response = send_chat_message(
                question=prompt,
                session_id=st.session_state.session_id,
                namespace=st.session_state.namespace
            )

        if response:
            # Add assistant message to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["answer"],
                "sources": response.get("sources", []),
                "metadata": response.get("metadata", {}),
                "timestamp": datetime.now().isoformat()
            })

            # Rerun to display new message
            st.rerun()
        else:
            st.error("Failed to get response. Please check API connection.")


# Main App
def main():
    """Main application entry point."""
    # Initialize session
    initialize_session()

    # Render UI
    render_sidebar()
    render_chat_interface()

    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption(f"Session: {st.session_state.session_id[:13]}...")

    with col2:
        st.caption(f"Namespace: {st.session_state.namespace}")

    with col3:
        st.caption("Powered by Groq & Pinecone")


if __name__ == "__main__":
    main()
