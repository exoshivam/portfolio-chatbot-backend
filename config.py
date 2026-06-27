import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    LM_STUDIO_BASE_URL = os.getenv(
        "LM_STUDIO_BASE_URL",
        "http://localhost:1234/v1"
    )

    LM_STUDIO_API_KEY = os.getenv(
        "LM_STUDIO_API_KEY",
        "lm-studio"
    )

    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "google/gemma-3-4b"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    VECTOR_DB_PATH = os.getenv(
        "VECTOR_DB_PATH",
        "data/faiss_index"
    )

    DOCS_PATH = os.getenv(
        "DOCS_PATH",
        "data/docs"
    )

    TOP_K = int(os.getenv("TOP_K", 3))