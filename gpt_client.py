# gpt_client.py
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GPTClient:
    def __init__(self, model: str | None = None):
        self.client = OpenAI()
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        print(f"[GPTClient] Koristim model: {self.model}")

    def ask(self, question: str) -> str:
        resp = self.client.responses.create(
            model=self.model,
            input=question.strip()
        )
        return resp.output_text

    def ask_with_prompt(self, question: str, prompt: str) -> str:
        full_input = f"{prompt.strip()}\n\nPitanje: {question.strip()}"
        resp = self.client.responses.create(
            model=self.model,
            input=full_input
        )
        return resp.output_text

    def describe_image_url(self, image_url: str, prompt: str | None = None) -> str:
        """
        Vision opis slike kada imamo PRAVI URL (Responses API očekuje image_url STRING).
        """
        user_text = (prompt or "Šta je na ovoj slici?").strip()

        resp = self.client.responses.create(
            model=self.model,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_text},
                    {"type": "input_image", "image_url": image_url}  # <- mora biti string
                ]
            }]
        )
        return resp.output_text

