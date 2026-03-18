from src.retrieval.retriever import Retriever
from src.llm.generator import AnswerGenerator
from src.retrieval.reranker import LLMReranker

def ask(query: str):
    retriever = Retriever()
    reranker = LLMReranker()
    generator = AnswerGenerator()

    # 1. retrieval
    retrieved_chunks = retriever.smart_retrieve(query, top_k=15)
    # print("\n=== RETRIEVED CHUNKS ===\n")
    # for i, c in enumerate(retrieved_chunks):
    #     print(f"[{i}] {c[1]} | {c[4]} | {c[3]}")
    #     print(c[2][:150])
    #     print("-" * 50)

    # 2. reranking
    reranked_chunks = reranker.rerank(query, retrieved_chunks)
    # print("\n=== RERANKER OUTPUT ===\n")
    # for i, c in enumerate(reranked_chunks):
    #     print(f"[{i}] {c[2][:120]}")

    # 3. generation
    answer, _ = generator.generate(query, reranked_chunks)

    print("\n=== ANSWER ===\n")
    print(answer.strip())

    print("\n=== SOURCES ===\n")
    for idx, c in enumerate(reranked_chunks):
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