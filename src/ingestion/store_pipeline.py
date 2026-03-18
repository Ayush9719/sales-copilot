from src.ingestion.embedder import Embedder
from src.storage.vector_store import VectorStore
from src.storage.metadata_store import MetadataStore

def store_chunks(chunks):
    embedder = Embedder()
    vector_store = VectorStore()
    metadata_store = MetadataStore()

    call_id = chunks[0].call_id
    if metadata_store.call_exists(call_id):
        print(f"[INFO] Call {call_id} already ingested. Skipping.")
        return

    texts = [c.text for c in chunks]
    embeddings = embedder.embed(texts)

    chunk_ids = [c.chunk_id for c in chunks]

    vector_store.add_embeddings(embeddings, chunk_ids)
    metadata_store.insert_chunks(chunks)

    vector_store.save()