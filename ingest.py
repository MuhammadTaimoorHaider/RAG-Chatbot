"""
CLI script for batch document ingestion.
Processes PDF, DOCX, TXT, and MD files and stores them in Pinecone.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm
from loguru import logger

# Import RAG components
from rag_chain import (
    DocumentProcessor,
    EmbeddingManager,
    VectorStoreManager,
    DocumentProcessingError,
    VectorStoreError
)
from config import settings


# Configure logger for CLI
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/ingest_{time:YYYY-MM-DD}.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG"
)


class DocumentIngestor:
    """Handles batch document ingestion."""

    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        self.document_processor = DocumentProcessor()
        self.embedding_manager = EmbeddingManager()
        self.vector_store_manager = VectorStoreManager()

        # Ensure index exists
        self.vector_store_manager.create_index()

        # Supported file types
        self.supported_extensions = settings.allowed_file_types.split(',')

        logger.info(f"DocumentIngestor initialized (namespace: {namespace})")

    def validate_file(self, file_path: str) -> bool:
        """Validate file type and existence."""
        file_path = Path(file_path)

        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return False

        if not file_path.is_file():
            logger.error(f"Not a file: {file_path}")
            return False

        extension = file_path.suffix.lstrip('.')
        if extension not in self.supported_extensions:
            logger.error(f"Unsupported file type: {extension}. Supported: {self.supported_extensions}")
            return False

        return True

    def load_document(self, file_path: str) -> List:
        """Load a single document based on file type."""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        try:
            if extension == '.pdf':
                return self.document_processor.load_pdf(str(file_path))
            elif extension == '.docx':
                return self.document_processor.load_docx(str(file_path))
            elif extension in ['.txt', '.md']:
                return self.document_processor.load_text(str(file_path))
            else:
                raise DocumentProcessingError(f"Unsupported file type: {extension}")
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {str(e)}")
            raise

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single file and return statistics."""
        try:
            # Validate
            if not self.validate_file(file_path):
                return {
                    "status": "failed",
                    "filename": str(file_path),
                    "error": "Validation failed"
                }

            # Load document
            documents = self.load_document(file_path)

            # Chunk documents
            chunks = self.document_processor.chunk_documents(documents)

            # Upsert to Pinecone
            result = self.vector_store_manager.upsert_documents(
                chunks,
                self.embedding_manager,
                namespace=self.namespace
            )

            return {
                "status": "success",
                "filename": Path(file_path).name,
                "chunks_created": len(chunks),
                "elapsed_time": result["elapsed_time"]
            }

        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            return {
                "status": "failed",
                "filename": Path(file_path).name,
                "error": str(e)
            }

    def process_batch(self, file_paths: List[str]) -> Dict[str, Any]:
        """Process multiple files with progress tracking."""
        results = {
            "total_files": len(file_paths),
            "successful": 0,
            "failed": 0,
            "total_chunks": 0,
            "details": []
        }

        with tqdm(total=len(file_paths), desc="Processing files") as pbar:
            for file_path in file_paths:
                result = self.process_file(file_path)
                results["details"].append(result)

                if result["status"] == "success":
                    results["successful"] += 1
                    results["total_chunks"] += result["chunks_created"]
                else:
                    results["failed"] += 1

                pbar.update(1)
                pbar.set_postfix({
                    "success": results["successful"],
                    "failed": results["failed"]
                })

        return results

    def ingest_directory(self, dir_path: str, recursive: bool = False) -> Dict[str, Any]:
        """Ingest all supported files from a directory."""
        dir_path = Path(dir_path)

        if not dir_path.exists() or not dir_path.is_dir():
            logger.error(f"Invalid directory: {dir_path}")
            return {"status": "failed", "error": "Invalid directory"}

        # Find all supported files
        file_paths = []
        if recursive:
            for ext in self.supported_extensions:
                file_paths.extend(dir_path.rglob(f"*.{ext}"))
        else:
            for ext in self.supported_extensions:
                file_paths.extend(dir_path.glob(f"*.{ext}"))

        if not file_paths:
            logger.warning(f"No supported files found in {dir_path}")
            return {"status": "success", "total_files": 0}

        logger.info(f"Found {len(file_paths)} files to process")
        return self.process_batch([str(f) for f in file_paths])


def print_results(results: Dict[str, Any]):
    """Pretty print ingestion results."""
    print("\n" + "=" * 60)
    print("INGESTION RESULTS")
    print("=" * 60)
    print(f"Total Files:     {results['total_files']}")
    print(f"Successful:      {results['successful']}")
    print(f"Failed:          {results['failed']}")
    print(f"Total Chunks:    {results['total_chunks']}")
    print("-" * 60)

    if results['failed'] > 0:
        print("\nFailed Files:")
        for detail in results['details']:
            if detail['status'] == 'failed':
                print(f"  - {detail['filename']}: {detail.get('error', 'Unknown error')}")

    print("\n" + "=" * 60)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ingest documents into the RAG system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ingest.py --file document.pdf
  python ingest.py --file report.docx --namespace project-alpha
  python ingest.py --directory ./docs --recursive
  python ingest.py --batch file1.pdf file2.txt file3.docx
        """
    )

    # File input options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--file',
        type=str,
        help='Path to a single file to ingest'
    )
    group.add_argument(
        '--directory',
        type=str,
        help='Path to directory containing files to ingest'
    )
    group.add_argument(
        '--batch',
        nargs='+',
        type=str,
        help='Multiple file paths to ingest'
    )

    # Optional arguments
    parser.add_argument(
        '--namespace',
        type=str,
        default='default',
        help='Pinecone namespace for document storage (default: default)'
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Recursively search directories (only with --directory)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Configure logging
    if args.verbose:
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")

    # Create logs directory
    os.makedirs("logs", exist_ok=True)

    try:
        # Initialize ingestor
        ingestor = DocumentIngestor(namespace=args.namespace)

        # Process based on input type
        if args.file:
            logger.info(f"Ingesting single file: {args.file}")
            result = ingestor.process_file(args.file)

            if result['status'] == 'success':
                print(f"\n✓ Successfully processed {result['filename']}")
                print(f"  Chunks created: {result['chunks_created']}")
                print(f"  Time: {result['elapsed_time']:.2f}s")
            else:
                print(f"\n✗ Failed to process {result['filename']}")
                print(f"  Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)

        elif args.directory:
            logger.info(f"Ingesting directory: {args.directory}")
            results = ingestor.ingest_directory(args.directory, recursive=args.recursive)
            print_results(results)

        elif args.batch:
            logger.info(f"Ingesting batch of {len(args.batch)} files")
            results = ingestor.process_batch(args.batch)
            print_results(results)

        logger.info("Ingestion completed successfully")

    except KeyboardInterrupt:
        logger.warning("Ingestion interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
