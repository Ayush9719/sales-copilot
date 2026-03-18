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
You are analyzing sales call transcripts.

Answer the question using ONLY the provided context.

Guidelines:
- Combine information across snippets
- Be concise and factual
- Do not assume information not present
- If information is partial, answer with available evidence
- If the query asks for negative feedback, focus on complaints, objections, or concerns.

---

Question:
{query}

---

Context:
{context}

---

Answer:
"""
    return prompt