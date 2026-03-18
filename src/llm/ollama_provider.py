import requests
from src.llm.base import BaseLLM

class OllamaLLM(BaseLLM):
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
        )
        return response.json()["response"]