# gpt_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Učitaj environment varijable iz .env fajla
load_dotenv()

class GPTClient:
    def __init__(self, model: str | None = None):
        self.client = OpenAI()
        # default model, možeš promeniti preko .env ako hoćeš
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def ask(self, question: str) -> str:
        """
        Poziva OpenAI Responses API i vraća plain text odgovor.
        """
        resp = self.client.responses.create(
            model=self.model,
            input=question.strip()
        )
        return resp.output_text
