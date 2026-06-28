import os
import pickle

import faiss
import numpy as np

from config import Config


class VectorStore:

    def __init__(self):
        self.index = None
        self.chunks = []

        index_path = os.path.join(
            Config.VECTOR_STORE_DIR, "faiss.index"
        )
        metadata_path = os.path.join(
            Config.VECTOR_STORE_DIR, "metadata.pkl"
        )

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)

        if os.path.exists(metadata_path):
            with open(metadata_path, "rb") as f:
                self.chunks = pickle.load(f)

    def is_ready(self):
        return (
            self.index is not None
            and len(self.chunks) > 0
        )

    def search(self, embedding, top_k, source_filter=None):
        if not self.is_ready():
            return []

        distances, indices = self.index.search(
            np.array(embedding, dtype=np.float32),
            top_k
        )
        print("\n===== SEARCH RESULTS =====")
        for score, idx in zip(distances[0], indices[0]):
            print(f"Score: {score:.4f}")
            if idx != -1:
                print(self.chunks[idx]["source"])
                print(self.chunks[idx]["text"][:200])
                print("-" * 60)        

        results = []

        for idx in indices[0]:
            if idx == -1:
                continue

            chunk = self.chunks[idx]

            if source_filter and chunk["source"] not in source_filter:
                continue

            results.append(chunk["text"])

        return results