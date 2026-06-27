from config import Config


class EmbeddingService:

    def __init__(self):
        self.model = None

    def encode(self, texts):
        if self.model is None:
            from sentence_transformers import SentenceTransformer
            print("Lazy loading embedding model...")
            self.model = SentenceTransformer(Config.EMBEDDING_MODEL)

        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings