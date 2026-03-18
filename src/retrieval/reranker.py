from src.llm.ollama_provider import OllamaLLM


class LLMReranker:
    def __init__(self):
        self.llm = OllamaLLM()

    def rerank(self, query: str, chunks: list, min_k: int = 2, max_k: int = 10):
        if not chunks:
            return []
        filtered_chunks = [
            c for c in chunks if not self._is_low_signal(c[2])
        ]
        if not filtered_chunks:
            filtered_chunks = chunks
        context = ""
        for idx, c in enumerate(filtered_chunks):
            context += f"\n[{idx}] {c[2]}\n"
        prompt = f"""
You are helping answer a user question from call transcripts.

Reorder the snippets that according to the usefulness for answering the question.

Guidelines:
- Prioritize snippets that directly address the question topic, even if wording differs (e.g., pricing may include discounts, cost, or financial terms).
- Prefer specific, actionable statements over general discussion
- Ignore introductions, recaps, or generic conversation
- Avoid redundant snippets
- Include supporting context only if it helps answer the question
- Return {min_k}-{max_k} indices

---

Question:
{query}

---

Context:
{context}

---

Output:
comma-separated indices (e.g., 1,3)
"""

        response = self.llm.generate(prompt).strip()
        try:
            indices = [int(x.strip()) for x in response.split(",")]
        except:
            indices = []

        selected = [
            filtered_chunks[i]
            for i in indices
            if 0 <= i < len(filtered_chunks)
        ]
        if len(selected) < min_k:
            selected = filtered_chunks[:max(min_k, min(len(filtered_chunks), max_k))]

        return selected[:max_k]

    def _is_low_signal(self, text: str) -> bool:
        text = text.lower()

        noise_patterns = [
            "good morning",
            "quick recap",
            "last week",
            "agenda",
            "thanks for joining",
            "let's get started",
        ]

        return any(p in text for p in noise_patterns)