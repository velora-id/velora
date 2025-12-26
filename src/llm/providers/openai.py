from .base import LLMProvider
from typing import Dict, Any
import openai

class OpenAIProvider(LLMProvider):
    def __init__(self, config: Dict[str, Any]):
        self.client = openai.OpenAI(api_key=config.get("api_key"))

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.completions.create(
            model="text-davinci-003",
            prompt=prompt,
            **kwargs
        )
        return response.choices[0].text.strip()

    def is_healthy(self) -> bool:
        try:
            self.client.models.list()
            return True
        except Exception:
            return False
