from src.llm.ollama_provider import OllamaLLM
from src.llm.prompt import build_prompt

class AnswerGenerator:
    def __init__(self):
        self.llm = OllamaLLM()

    def generate(self, query: str, chunks: list):
        prompt = build_prompt(query, chunks)
        response = self.llm.generate(prompt)
        used_indices = self._extract_used_indices(response)
        if not used_indices:
            used_indices = list(range(min(3, len(chunks))))
        return response, used_indices

    def _extract_used_indices(self, response: str):
        import re
        match = re.search(r"\[(.*?)\]", response)
        if not match:
            return []
        try:
            return [int(x.strip()) for x in match.group(1).split(",")]
        except:
            return []