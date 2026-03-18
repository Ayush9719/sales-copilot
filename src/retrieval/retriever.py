from src.ingestion.embedder import Embedder
from src.storage.vector_store import VectorStore
from src.storage.metadata_store import MetadataStore
from src.retrieval.filters import parse_query

class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.metadata_store = MetadataStore()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        stage: str = None,
        tags: list = None,
        speaker: str = None,
    ):
        # 1. embed query
        query_embedding = self.embedder.embed([query])

        # 2. semantic search
        chunk_ids = self.vector_store.search(query_embedding, top_k=top_k)

        # 3. metadata filtering
        results = self.metadata_store.filter_chunks(
            chunk_ids=chunk_ids,
            stage=stage,
            tags=tags,
            speaker=speaker,
        )

        return results

    def stitch_context(self, rows):
        stitched = []
        seen = set()
        for row in rows:
            call_id = row[1]
            seq_id = row[7]
            neighbor_ids = [seq_id - 1, seq_id, seq_id + 1]
            neighbors = self.metadata_store.get_chunks_by_sequence(call_id, neighbor_ids)
            for n in neighbors:
                key = (n[1], n[7])  # call_id + sequence_id
                if key not in seen:
                    seen.add(key)
                    stitched.append(n)
        stitched.sort(key=lambda x: (x[1], x[7]))
        return stitched

    def smart_retrieve(self, query: str, top_k=8):
        filters = parse_query(query)
        rows = self.retrieve(
            query=query,
            top_k=top_k,
            stage=filters["stage"],
            tags=filters["tags"],
        )
        stitched = self.stitch_context(rows)
        return stitched[:6]