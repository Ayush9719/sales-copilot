import re
from src.retrieval.retriever import Retriever
from src.llm.generator import AnswerGenerator
from src.retrieval.reranker import LLMReranker
from src.storage.metadata_store import MetadataStore

def _clean_source_text(text: str, speaker: str) -> str:
    pattern = rf"^{re.escape(speaker.strip())}\s*:\s*"
    return re.sub(pattern, "", text.strip(), count=1)

def print_sources(chunks):
    print("\n=== SOURCES ===\n")
    for idx, c in enumerate(chunks):
        cleaned_text = _clean_source_text(c[2], c[3])
        print(f"[{idx}] {c[1]} | {c[4]} | {c[3]}: {cleaned_text[:120]}")

def select_sources_by_indices(chunks, indices):
    selected = []
    seen = set()

    for i in indices:
        if isinstance(i, int) and 0 <= i < len(chunks) and i not in seen:
            selected.append(chunks[i])
            seen.add(i)

    return selected

def ask(query: str):
    retriever = Retriever()
    # reranker = LLMReranker()
    generator = AnswerGenerator()

    retrieved_chunks = retriever.smart_retrieve(query, top_k=15)
    # reranked_chunks = reranker.rerank(query, retrieved_chunks)
    answer, used_indices = generator.generate(query, retrieved_chunks)

    final_sources = select_sources_by_indices(retrieved_chunks, used_indices)
    if not final_sources:
        final_sources = retrieved_chunks[:3]

    print("\n=== ANSWER ===\n")
    print(answer.strip())
    print_sources(final_sources)

def summarize_call(query: str):
    store = MetadataStore()
    generator = AnswerGenerator()

    call_id = store.get_last_call_id()
    if not call_id:
        print("\n=== SUMMARY ===\n")
        print("No calls found.")
        return

    chunks = store.get_chunks_by_call_id(call_id)

    answer, used_indices = generator.generate_summary(call_id, chunks)

    final_sources = select_sources_by_indices(chunks, used_indices)
    if not final_sources:
        final_sources = chunks[:3]

    print("\n=== SUMMARY ===\n")
    print(answer.strip())
    print_sources(final_sources)