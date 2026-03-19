from src.ingestion.parser import parse_transcript

def test_parse_transcript_multiline(tmp_path):
    p = tmp_path / "call.txt"
    p.write_text(
        "[00:01] AE (John): Hello there\n"
        "continuation line\n"
        "[00:05] Prospect: Pricing seems high\n",
        encoding="utf-8",
    )

    rows = parse_transcript(str(p))
    assert len(rows) == 2
    assert rows[0]["speaker"] == "AE (John)"
    assert "continuation line" in rows[0]["text"]