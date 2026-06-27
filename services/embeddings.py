import voyageai

from config import Config


class EmbeddingService:

    def __init__(self):
        self.client = voyageai.Client(
            api_key=Config.VOYAGE_API_KEY
        )

    def encode_documents(self, texts):

        if isinstance(texts, str):
            texts = [texts]

        result = self.client.embed(
            texts,
            model="voyage-3-lite",
            input_type="document"
        )

        return result.embeddings

    def encode_query(self, text):

        result = self.client.embed(
            [text],
            model="voyage-3-lite",
            input_type="query"
        )

        return result.embeddings