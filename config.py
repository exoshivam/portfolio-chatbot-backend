import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Groq API
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    # Embedding model (local, sentence-transformers)
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # Chunking parameters
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

    # Paths
    VECTOR_STORE_DIR = os.getenv(
        "VECTOR_STORE_DIR",
        "vector_store"
    )
    DOCS_PATH = os.getenv(
        "DOCS_PATH",
        "data/docs"
    )

    # Retrieval
    TOP_K = int(os.getenv("TOP_K", 3))