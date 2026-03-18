def parse_query(query: str):
    query_lower = query.lower()

    stage = None
    if "pricing" in query_lower:
        stage = "pricing"
    elif "demo" in query_lower:
        stage = "demo"
    elif "objection" in query_lower:
        stage = "objection"
    elif "negotiation" in query_lower:
        stage = "negotiation"

    tags = []
    if any(k in query_lower for k in ["price", "discount", "cost"]):
        tags.append("pricing")

    if any(k in query_lower for k in ["security", "compliance"]):
        tags.append("security")

    return {
        "stage": stage,
        "tags": tags or None,
    }