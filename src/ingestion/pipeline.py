from src.ingestion.parser import parse_transcript
from src.ingestion.chunker import chunk_transcript
from src.ingestion.utils import extract_metadata

def ingest(file_path: str):
    call_id, stage = extract_metadata(file_path)
    parsed = parse_transcript(file_path)
    chunks = chunk_transcript(parsed, call_id, stage)
    return chunks