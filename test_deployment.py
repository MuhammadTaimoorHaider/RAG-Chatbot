#!/usr/bin/env python3
"""
Quick test script to verify RAG system is working before deployment.
Run this to ensure everything is configured correctly.
"""

import os
import sys
from pathlib import Path

def check_env_vars():
    """Check if required environment variables are set."""
    print("\n🔍 Checking environment variables...")

    required_vars = {
        "GROQ_API_KEY": "Groq API key",
        "PINECONE_API_KEY": "Pinecone API key",
        "PINECONE_ENVIRONMENT": "Pinecone environment",
        "PINECONE_INDEX_NAME": "Pinecone index name"
    }

    missing = []
    for var, description in required_vars.items():
        if os.getenv(var):
            print(f"  ✅ {var}: Set")
        else:
            print(f"  ❌ {var}: Missing")
            missing.append(var)

    if missing:
        print(f"\n❌ Missing required variables: {', '.join(missing)}")
        print("💡 Set them in your .env file")
        return False

    print("✅ All required environment variables are set!")
    return True


def check_files():
    """Check if required files exist."""
    print("\n🔍 Checking required files...")

    required_files = [
        "config.py",
        "rag_chain.py",
        "main.py",
        "app.py",
        "requirements.txt",
        "Dockerfile.huggingface"
    ]

    missing = []
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}: Missing")
            missing.append(file)

    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False

    print("✅ All required files present!")
    return True


def check_dependencies():
    """Check if key dependencies are installed."""
    print("\n🔍 Checking Python dependencies...")

    dependencies = {
        "fastapi": "FastAPI",
        "streamlit": "Streamlit",
        "langchain": "LangChain",
        "pinecone": "Pinecone",
        "groq": "Groq",
        "redis": "Redis",
    }

    missing = []
    for package, name in dependencies.items():
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name}: Not installed")
            missing.append(package)

    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("💡 Run: pip install -r requirements.txt")
        return False

    print("✅ All dependencies installed!")
    return True


def test_config():
    """Test configuration loading."""
    print("\n🔍 Testing configuration...")

    try:
        from config import settings
        print(f"  ✅ Config loaded successfully")
        print(f"  ✅ Groq Model: {settings.groq_model}")
        print(f"  ✅ Embedding Model: {settings.embedding_model}")
        print(f"  ✅ Pinecone Index: {settings.pinecone_index_name}")
        return True
    except Exception as e:
        print(f"  ❌ Config loading failed: {str(e)}")
        return False


def test_imports():
    """Test critical imports."""
    print("\n🔍 Testing critical imports...")

    try:
        from rag_chain import initialize_rag_system
        print("  ✅ RAG chain imports")
    except Exception as e:
        print(f"  ❌ RAG chain import failed: {str(e)}")
        return False

    try:
        from main import app
        print("  ✅ FastAPI app imports")
    except Exception as e:
        print(f"  ❌ FastAPI import failed: {str(e)}")
        return False

    print("✅ All imports successful!")
    return True


def check_api_keys():
    """Validate API keys format (not actually calling APIs)."""
    print("\n🔍 Validating API key formats...")

    groq_key = os.getenv("GROQ_API_KEY", "")
    if groq_key.startswith("gsk_"):
        print("  ✅ Groq API key format looks correct")
    else:
        print("  ⚠️  Groq API key format unusual (should start with gsk_)")

    pinecone_key = os.getenv("PINECONE_API_KEY", "")
    if len(pinecone_key) > 20:
        print("  ✅ Pinecone API key format looks correct")
    else:
        print("  ⚠️  Pinecone API key seems too short")

    return True


def main():
    """Run all checks."""
    print("="*60)
    print("🧪 RAG CHATBOT - PRE-DEPLOYMENT TEST")
    print("="*60)

    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Run all checks
    checks = [
        ("Environment Variables", check_env_vars),
        ("Required Files", check_files),
        ("Dependencies", check_dependencies),
        ("Configuration", test_config),
        ("Imports", test_imports),
        ("API Keys Format", check_api_keys),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} check crashed: {str(e)}")
            results.append((name, False))

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")

    print(f"\n📈 Score: {passed}/{total} checks passed")

    if passed == total:
        print("\n🎉 ALL CHECKS PASSED!")
        print("✅ Your project is ready for deployment!")
        print("\n🚀 Next steps:")
        print("  1. Read: DEPLOY_HUGGINGFACE_COMPLETE.md")
        print("  2. Create HF Space")
        print("  3. Upload files")
        print("  4. Add secrets")
        print("  5. Deploy!")
    else:
        print("\n⚠️  SOME CHECKS FAILED")
        print("❌ Fix the issues above before deploying")
        print("\n💡 Common fixes:")
        print("  - Run: pip install -r requirements.txt")
        print("  - Copy .env.example to .env and add your API keys")
        print("  - Verify all files are present")

    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test crashed: {str(e)}")
        sys.exit(1)
