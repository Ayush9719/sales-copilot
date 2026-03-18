def detect_intent(query: str):
    q = query.lower()

    if "list" in q and "call" in q:
        return "list_calls"

    if "summarise" in q or "summarize" in q:
        return "summarize"

    if "negative" in q or "complaint" in q:
        return "negative_feedback"

    return "qa"