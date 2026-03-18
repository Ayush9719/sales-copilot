from src.llm.ollama_provider import OllamaLLM

class LLMReranker:
    def __init__(self):
        self.llm = OllamaLLM()

    def rerank(self, query: str, chunks: list, min_k: int = 2, max_k: int = 5):
        if not chunks:
            return []

        context = ""
        for idx, c in enumerate(chunks):
            context += f"\n[{idx}] {c[2]}\n"

        prompt = f"""
You are a sales analyst.

Select the most useful snippets for answering the question.

Guidelines:
- Prefer directly relevant snippets
- Include supporting context if needed
- Avoid redundant snippets
- Return {min_k}-{max_k} indices

---

Question:
{query}

---

Context:
{context}

---

Answer:
comma-separated indices
"""

        response = self.llm.generate(prompt).strip()

        try:
            indices = [int(x.strip()) for x in response.split(",")]
        except:
            indices = []

        selected = [chunks[i] for i in indices if i < len(chunks)]

        if len(selected) < min_k:
            selected = chunks[:max(min_k, min(len(chunks), max_k))]

        return selected[:max_k]