import os
import pickle

import faiss
import numpy as np

from config import Config
from services.embeddings import EmbeddingService
from utils.helpers import load_documents


def main():

    documents = load_documents(
        Config.DOCS_PATH
    )

    if not documents:
        print("No documents found.")
        return

    embedder = EmbeddingService()

    embeddings = embedder.encode(documents)

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    os.makedirs(
        os.path.dirname(Config.VECTOR_DB_PATH),
        exist_ok=True
    )

    faiss.write_index(
        index,
        Config.VECTOR_DB_PATH + ".index"
    )

    with open(
        Config.VECTOR_DB_PATH + ".pkl",
        "wb"
    ) as f:
        pickle.dump(documents, f)

    print(f"Indexed {len(documents)} documents.")


if __name__ == "__main__":
    main()