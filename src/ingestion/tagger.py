def extract_tags(text: str):
    text_lower = text.lower()

    tags = []

    if any(k in text_lower for k in ["price", "pricing", "discount", "cost"]):
        tags.append("pricing")

    if any(k in text_lower for k in ["security", "soc", "encryption", "compliance"]):
        tags.append("security")

    if any(k in text_lower for k in ["competitor", "competitors"]):
        tags.append("competition")

    if any(k in text_lower for k in ["objection", "concern", "issue"]):
        tags.append("objection")

    return tags