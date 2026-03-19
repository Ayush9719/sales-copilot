import uuid
from typing import List, Dict
from src.models.schema import Chunk
from src.ingestion.tagger import extract_tags

def chunk_transcript(
    parsed_data: List[Dict],
    call_id: str,
    stage: str,
) -> List[Chunk]:
    chunks = []

    for idx, entry in enumerate(parsed_data):
        speaker = entry["speaker"].strip()
        text = entry["text"].strip()
        chunk = Chunk(
            chunk_id        = str(uuid.uuid4()),
            call_id         = call_id,
            text            = text,
            speaker         = speaker,
            timestamp       = entry["timestamp"],
            sequence_id     = idx,
            stage           = stage,
            tags            = extract_tags(f"{speaker}: {text}"),
        )
        chunks.append(chunk)
    return chunks