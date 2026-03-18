from src.retrieval.retriever import Retriever
from src.llm.generator import AnswerGenerator
from src.llm.prompt import build_prompt

def ask(query: str):
    retriever = Retriever()
    generator = AnswerGenerator()
    chunks = retriever.smart_retrieve(query)
    answer = generator.generate(query, chunks)

    print("\n=== ANSWER ===\n")
    print(answer)

    print("\n=== SOURCES ===\n")
    for idx, c in enumerate(chunks):
        print(f"[{idx}] {c[1]} | {c[4]} | {c[3]}: {c[2][:100]}")