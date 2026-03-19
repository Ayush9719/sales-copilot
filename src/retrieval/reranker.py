import json
import re
from typing import List
from src.llm.ollama_provider import OllamaLLM


class LLMReranker:
    def __init__(self):
        self.llm = OllamaLLM()

    def rerank(self, query: str, chunks: list, min_k: int = 2, max_k: int = 5) -> list:
        """
        Returns a reranked subset of the input chunks.

        Expects the model to return JSON like:
        {
          "selected_indices": [1, 0, 3]
        }
        """
        if not chunks:
            return []

        capped_chunks = chunks[: min(len(chunks), 12)]

        context_parts = []
        for idx, c in enumerate(capped_chunks):
            context_parts.append(
                f"""[{idx}]
Call ID: {c[1]}
Timestamp: {c[4]}
Speaker: {c[3]}
Text: {c[2]}
"""
            )
        context = "\n".join(context_parts)

        prompt = f"""
You are a sales call retrieval reranker.

Your job is to select the most useful transcript snippets for answering the user's question.

Instructions:
- Prefer snippets that directly answer the question.
- Keep supporting context only if it helps the final answer.
- Avoid redundant snippets.
- Return between {min_k} and {max_k} snippet indices.
- Return ONLY valid JSON.
- Do not include any explanation.

Return exactly:
{{
  "selected_indices": [0, 2, 4]
}}

Question:
{query}

Candidate snippets:
{context}
""".strip()

        response = self.llm.generate(prompt)
        parsed = self._safe_parse_response(response)

        indices = self._normalize_indices(
            parsed.get("selected_indices", []),
            total_chunks=len(capped_chunks),
        )

        selected = [capped_chunks[i] for i in indices]

        if len(selected) < min_k:
            selected = capped_chunks[: max(min_k, min(len(capped_chunks), max_k))]

        return selected[:max_k]

    def _safe_parse_response(self, response: str) -> dict:
        text = response.strip()

        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if fenced_match:
            candidate = fenced_match.group(1)
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            candidate = json_match.group(0)
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        return {}

    def _normalize_indices(self, indices, total_chunks: int) -> List[int]:
        if not isinstance(indices, list):
            return []

        cleaned = []
        for item in indices:
            try:
                idx = int(item)
            except Exception:
                continue

            if 0 <= idx < total_chunks and idx not in cleaned:
                cleaned.append(idx)

        return cleaned