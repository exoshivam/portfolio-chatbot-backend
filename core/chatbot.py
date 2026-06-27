from core.llm import LLM
from core.memory import ConversationMemory
from core.prompt import build_prompt
from services.rag import RAGService


class Chatbot:

    def __init__(self):
        self.memory = ConversationMemory()
        self.llm = LLM()
        self.rag = RAGService()

    def chat(self, message: str) -> str:

        context = self.rag.retrieve(message)

        messages = build_prompt(
            history=self.memory.get_history(),
            context=context,
            question=message
        )

        answer = self.llm.generate(messages)

        self.memory.add_user_message(message)
        self.memory.add_assistant_message(answer)

        return answer