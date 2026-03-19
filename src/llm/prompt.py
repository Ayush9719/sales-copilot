def build_prompt(query: str, chunks: list) -> str:
    context_lines = []
    for i, chunk in enumerate(chunks):
        text = chunk[2]
        call_id = chunk[1]
        speaker = chunk[3]
        timestamp = chunk[4]
        context_lines.append(
            f"[{i}] call_id={call_id} speaker={speaker} timestamp={timestamp}\n{text}"
        )

    context = "\n\n".join(context_lines)

    return f"""
You are a sales copilot assistant.

Answer the user's question using only the context below.
If the answer is not supported by the context, say that clearly.
Use only source indices that directly support the answer.
Return a concise but complete answer in 2-4 sentences.
Do not include any text outside the JSON object.

Return ONLY valid JSON in exactly this shape:
{{
  "answer": "your grounded answer",
  "source_indices": [0, 2]
}}

User question:
{query}

Context:
{context}
""".strip()


def build_summary_prompt(call_id: str, chunks: list) -> str:
    context_lines = []
    for i, chunk in enumerate(chunks):
        text = chunk[2]
        speaker = chunk[3]
        timestamp = chunk[4]
        context_lines.append(
            f"[{i}] speaker={speaker} timestamp={timestamp}\n{text}"
        )

    context = "\n\n".join(context_lines)

    return f"""
You are a sales copilot assistant.

Summarize this sales call for an account executive.
Focus on:
- customer goals and pain points
- objections or concerns
- pricing/commercial discussion
- legal/security concerns
- next steps and decision signals

Use only the context below.
Do not answer a narrow sub-question.
Produce a call-level summary in 4-7 sentences.
Use only source indices that directly support the summary.
Do not include any text outside the JSON object.

Return ONLY valid JSON in exactly this shape:
{{
  "answer": "call summary here",
  "source_indices": [0, 3, 8]
}}

Call ID:
{call_id}

Context:
{context}
""".strip()