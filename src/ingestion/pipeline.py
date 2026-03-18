from src.ingestion.parser import parse_transcript
from src.ingestion.chunker import chunk_transcript

def ingest(file_path: str, call_id: str, stage: str):
    parsed = parse_transcript(file_path)
    chunks = chunk_transcript(parsed, call_id, stage)
    return chunks