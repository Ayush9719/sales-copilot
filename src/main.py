from src.retrieval.retriever import Retriever
from src.llm.generator import AnswerGenerator
from src.retrieval.reranker import LLMReranker

def ask(query: str):
    retriever = Retriever()
    reranker = LLMReranker()
    generator = AnswerGenerator()

    # 1. retrieval
    retrieved_chunks = retriever.smart_retrieve(query, top_k=10)

    # 2. reranking (self-healing)
    reranked_chunks = reranker.rerank(query, retrieved_chunks)

    # 3. generation (self-healing)
    answer, used_indices = generator.generate(query, reranked_chunks)

    final_sources = [
        reranked_chunks[i]
        for i in used_indices
        if i < len(reranked_chunks)
    ]

    print("\n=== ANSWER ===\n")
    print(answer.strip())

    print("\n=== SOURCES ===\n")
    for idx, c in enumerate(final_sources):
        print(f"[{idx}] {c[1]} | {c[4]} | {c[3]}: {c[2][:120]}")

def summarize_call(query: str):
    retriever = Retriever()
    generator = AnswerGenerator()

    # retrieve all chunks (or high top_k)
    chunks = retriever.smart_retrieve(query, top_k=15)

    answer, _ = generator.generate(
        "Summarize the key points of this call", chunks
    )

    print("\n=== SUMMARY ===\n")
    print(answer.strip())