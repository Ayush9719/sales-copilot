import json
import re
from typing import List, Tuple

from src.llm.ollama_provider import OllamaLLM
from src.llm.prompt import build_prompt, build_summary_prompt


class AnswerGenerator:
    def __init__(self):
        self.llm = OllamaLLM()

    def generate(self, query: str, chunks: list) -> Tuple[str, List[int]]:
        if not chunks:
            return "I could not find any relevant transcript snippets.", []

        prompt = build_prompt(query, chunks)
        response = self.llm.generate(prompt)

        parsed = self._safe_parse_response(response)

        answer = parsed.get("answer", "").strip()
        used_indices = self._normalize_indices(
            parsed.get("source_indices", []),
            total_chunks=len(chunks),
        )

        if not answer:
            answer = response.strip()

        if not used_indices:
            used_indices = list(range(min(3, len(chunks))))

        return answer, used_indices

    def generate_summary(self, call_id: str, chunks: list) -> Tuple[str, List[int]]:
        if not chunks:
            return "I could not find any transcript snippets for this call.", []

        prompt = build_summary_prompt(call_id, chunks)
        response = self.llm.generate(prompt)

        parsed = self._safe_parse_response(response)

        answer = parsed.get("answer", "").strip()
        used_indices = self._normalize_indices(
            parsed.get("source_indices", []),
            total_chunks=len(chunks),
        )

        if not answer:
            answer = response.strip()

        if not used_indices:
            used_indices = list(range(min(5, len(chunks))))

        return answer, used_indices

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