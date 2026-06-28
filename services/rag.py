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

        question_lower = question.lower()

        source_filter = None

        # Project-related queries
        if any(word in question_lower for word in [
            "project",
            "projects",
            "portfolio chatbot",
            "position doctor",
            "career mentor",
            "rural school attendance",
            "attendance",
            "mood tracker",
            "glue",
            "call break",
            "stock",
            "doctor",
            "chatbot"
        ]):
            source_filter = ["projects.md"]

        # Skills
        elif any(word in question_lower for word in [
            "skill",
            "skills",
            "tech stack",
            "technology",
            "language",
            "languages",
            "frontend",
            "backend",
            "framework",
            "react",
            "node",
            "python",
            "mongodb",
            "fastapi"
        ]):
            source_filter = ["skills.md"]

        # Education & Experience
        elif any(word in question_lower for word in [
            "education",
            "college",
            "school",
            "cgpa",
            "experience",
            "internship",
            "certificate",
            "certification",
            "certifications"
        ]):
            source_filter = ["about.md", "experience.md"]

        # Contact
        elif any(word in question_lower for word in [
            "contact",
            "email",
            "phone",
            "linkedin",
            "github",
            "freelance",
            "hire"
        ]):
            source_filter = ["faq.md", "about.md"]

        embedding = self.embedder.encode_query(question)

        # Search only filtered files
        docs = self.vectorstore.search(
            embedding,
            Config.TOP_K,
            source_filter
        )

        # Fallback to all documents
        if not docs and source_filter:
            docs = self.vectorstore.search(
                embedding,
                Config.TOP_K
            )

        if not docs:
            return ""

        context = "\n\n".join(docs)

        print("\n========== RETRIEVED CONTEXT ==========\n")
        print(context)
        print("\n=======================================\n")

        return context