import sqlite3
import json
from typing import List
from src.models.schema import Chunk
from src.utils.config import Config

class MetadataStore:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DB_PATH)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS chunks (
            chunk_id TEXT PRIMARY KEY,
            call_id TEXT,
            text TEXT,
            speaker TEXT,
            timestamp TEXT,
            stage TEXT,
            tags TEXT,
            sequence_id INTEGER
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def call_exists(self, call_id: str):
        query = "SELECT 1 FROM chunks WHERE call_id = ? LIMIT 1"
        result = self.conn.execute(query, (call_id,)).fetchone()
        return result is not None

    def insert_chunks(self, chunks: List[Chunk]):
        query = """
        INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        data = [
            (
                c.chunk_id,
                c.call_id,
                c.text,
                c.speaker,
                c.timestamp,
                c.stage,
                json.dumps(c.tags),
                getattr(c, "sequence_id", 0),
            )
            for c in chunks
        ]
        self.conn.executemany(query, data)
        self.conn.commit()

    def get_chunks_by_ids(self, chunk_ids: List[str]):
        query = f"""
        SELECT * FROM chunks WHERE chunk_id IN ({','.join(['?']*len(chunk_ids))})
        """
        rows = self.conn.execute(query, chunk_ids).fetchall()
        return rows