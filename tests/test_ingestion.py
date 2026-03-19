from src.ingestion.pipeline import ingest

def test_ingestion(tmp_path):
    p = tmp_path / "call.txt"
    p.write_text(
        "[00:01] AE: Hello\n"
        "[00:03] Prospect: Pricing is expensive\n",
        encoding="utf-8",
    )

    chunks = ingest(str(p))
    assert len(chunks) > 0