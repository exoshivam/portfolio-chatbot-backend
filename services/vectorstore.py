import os
import pickle

import faiss
import numpy as np

from config import Config


class VectorStore:

    def __init__(self):

        self.index = None
        self.documents = []

        index_path = Config.VECTOR_DB_PATH + ".index"
        docs_path = Config.VECTOR_DB_PATH + ".pkl"

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)

        if os.path.exists(docs_path):
            with open(docs_path, "rb") as f:
                self.documents = pickle.load(f)

    def is_ready(self):
        return self.index is not None and len(self.documents) > 0

    def search(self, embedding, top_k):

        if not self.is_ready():
            return []

        distances, indices = self.index.search(
            np.array(embedding, dtype=np.float32),
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx == -1:
                continue

            results.append(
                self.documents[idx]
            )

        return results