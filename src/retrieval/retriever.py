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

    def smart_retrieve(self, query: str, top_k=5):
        filters = parse_query(query)
        return self.retrieve(
            query=query,
            top_k=top_k,
            stage=filters["stage"],
            tags=filters["tags"],
        )