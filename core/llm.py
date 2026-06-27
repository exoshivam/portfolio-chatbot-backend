from openai import OpenAI

from config import Config


class LLM:

    def __init__(self):
        self.client = OpenAI(
            base_url=Config.LM_STUDIO_BASE_URL,
            api_key=Config.LM_STUDIO_API_KEY
        )
        self.groq_client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=Config.GROQ_API_KEY
        )

    def generate(self, messages):
        try:
            # Try the local LLM first (timeout is set high because if the server is offline, it fails instantly anyway. If it's online, it needs time to generate)
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=messages,
                temperature=0.4,
                timeout=60.0
            )
        except Exception as e:
            print(f"Local LLM failed ({e}). Falling back to Groq API...")
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.4
            )
        
        return response.choices[0].message.content.strip()