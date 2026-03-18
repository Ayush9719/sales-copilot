import faiss
import numpy as np
import os
import json
from src.utils.config import Config

class VectorStore:
    def __init__(self):
        self.index_path = Config.FAISS_INDEX_PATH
        self.mapping_path = self.index_path + ".mapping.json"

        self.index = None
        self.id_mapping = []

        self._load_or_create()

    def _load_or_create(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.mapping_path, "r") as f:
                self.id_mapping = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(Config.VECTOR_DIM)
            self.id_mapping = []

    def add_embeddings(self, embeddings: np.ndarray, chunk_ids: list):
        self.index.add(embeddings)
        self.id_mapping.extend(chunk_ids)

    def search(self, query_embedding: np.ndarray, top_k=5):
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.id_mapping):
                results.append(self.id_mapping[idx])

        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.mapping_path, "w") as f:
            json.dump(self.id_mapping, f)