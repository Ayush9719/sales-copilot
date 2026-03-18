from src.retrieval.retriever import Retriever

def test_retrieval():
    r = Retriever()
    results = r.smart_retrieve("pricing concerns")
    assert len(results) > 0