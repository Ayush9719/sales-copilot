from src.llm.ollama_provider import OllamaLLM
from src.llm.prompt import build_prompt

class AnswerGenerator:
    def __init__(self):
        self.llm = OllamaLLM()

    def generate(self, query: str, chunks: list):
        prompt = build_prompt(query, chunks)
        response = self.llm.generate(prompt)
        return response
    
    def format_sources(chunks):
        sources = []
        for idx, c in enumerate(chunks):
            sources.append(
                f"[{idx}] {c[1]} | {c[4]} | {c[3]}: {c[2][:100]}"
            )
        return "\n".join(sources)