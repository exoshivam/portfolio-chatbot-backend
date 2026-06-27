from openai import OpenAI

from config import Config


class LLM:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=Config.GROQ_API_KEY
        )

    def generate(self, messages):
        response = self.client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=messages,
            temperature=0.4
        )

        return response.choices[0].message.content.strip()