import os
import pickle

import faiss
import numpy as np

from config import Config
from services.embeddings import EmbeddingService
from utils.helpers import chunk_documents


def main():
    print("Loading and chunking documents...")

    chunks = chunk_documents(Config.DOCS_PATH)

    if not chunks:
        print("No documents found.")
        return

    print(f"Found {len(chunks)} chunks from docs:")
    sources = set(c["source"] for c in chunks)
    for src in sorted(sources):
        count = sum(
            1 for c in chunks if c["source"] == src
        )
        print(f"  {src}: {count} chunks")

    print("\nLoading embedding model...")
    embedder = EmbeddingService()

    texts = [c["text"] for c in chunks]
    print("Generating embeddings...")
    embeddings = embedder.encode(texts)

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    # Save to vector_store/
    os.makedirs(Config.VECTOR_STORE_DIR, exist_ok=True)

    index_path = os.path.join(
        Config.VECTOR_STORE_DIR, "faiss.index"
    )
    metadata_path = os.path.join(
        Config.VECTOR_STORE_DIR, "metadata.pkl"
    )

    faiss.write_index(index, index_path)

    with open(metadata_path, "wb") as f:
        pickle.dump(chunks, f)

    print(f"\nSaved {len(chunks)} chunks to:")
    print(f"  {index_path}")
    print(f"  {metadata_path}")
    print("Done!")


if __name__ == "__main__":
    main()