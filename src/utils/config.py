import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

    DB_PATH = os.getenv("DB_PATH", "data/metadata.db")
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "data/faiss.index")

    VECTOR_DIM = 384