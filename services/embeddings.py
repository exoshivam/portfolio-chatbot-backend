from sentence_transformers import SentenceTransformer

from config import Config


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            Config.EMBEDDING_MODEL
        )

    def encode(self, texts):

        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings