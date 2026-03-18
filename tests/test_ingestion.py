from src.ingestion.pipeline import ingest

def test_ingestion():
    chunks = ingest("data/1_demo_call.txt")
    assert len(chunks) > 0