from sentence_transformers import SentenceTransformer

class Embedder:
    _model = None

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        if Embedder._model is None:
            Embedder._model = SentenceTransformer(model_name)
        self.model = Embedder._model

    def embed(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)