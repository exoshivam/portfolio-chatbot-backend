from config import Config
from services.embeddings import EmbeddingService
from services.vectorstore import VectorStore


class RAGService:

    def __init__(self):
        self.embedder = EmbeddingService()
        self.vectorstore = VectorStore()

    def retrieve(self, question: str) -> str:

        if not self.vectorstore.is_ready():
            return ""

        embedding = self.embedder.encode(question)

        docs = self.vectorstore.search(
            embedding,
            Config.TOP_K
        )

        if not docs:
            return ""

        return "\n\n".join(docs)