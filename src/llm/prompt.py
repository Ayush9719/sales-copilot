def build_prompt(query: str, chunks: list):
    context = ""

    for idx, chunk in enumerate(chunks):
        context += f"""
[{idx}]
Call ID: {chunk[1]}
Timestamp: {chunk[4]}
Speaker: {chunk[3]}
Text: {chunk[2]}
"""

    prompt = f"""
You are a sales assistant AI.
Answer the user query using ONLY the provided context.
If the answer is not present, say "I don't know".
Provide:
1. A clear answer
2. Bullet points if needed
3. Cite sources using [index] references
---
Query:
{query}
---
Context:
{context}
---
Answer:
"""
    return prompt