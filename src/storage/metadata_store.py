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
    
    def filter_chunks(
        self,
        chunk_ids=None,
        stage=None,
        tags=None,
        speaker=None,
    ):
        query = "SELECT * FROM chunks WHERE 1=1"
        params = []

        if chunk_ids:
            query += f" AND chunk_id IN ({','.join(['?']*len(chunk_ids))})"
            params.extend(chunk_ids)

        if stage:
            query += " AND stage = ?"
            params.append(stage)

        if speaker:
            query += " AND speaker LIKE ?"
            params.append(f"%{speaker}%")

        rows = self.conn.execute(query, params).fetchall()

        # tag filtering (post-process since stored as JSON)
        results = []
        for row in rows:
            row_tags = json.loads(row[6])
            if tags:
                if not any(tag in row_tags for tag in tags):
                    continue
            results.append(row)

        return results
    
    def list_calls(self):
        query = """
        SELECT call_id
        FROM chunks
        GROUP BY call_id
        ORDER BY MAX(rowid) DESC
        """
        rows = self.conn.execute(query).fetchall()
        return [r[0] for r in rows]
    
    def get_chunks_by_sequence(
        self,
        call_id: str,
        sequence_ids: list
    ):
        query = f"""
        SELECT * FROM chunks
        WHERE call_id = ?
        AND sequence_id IN ({','.join(['?'] * len(sequence_ids))})
        ORDER BY sequence_id
        """
        params = [call_id] + sequence_ids
        return self.conn.execute(query, params).fetchall()
    
    def get_last_call_id(self):
        query = """
        SELECT call_id
        FROM chunks
        GROUP BY call_id
        ORDER BY MAX(rowid) DESC
        LIMIT 1
        """
        row = self.conn.execute(query).fetchone()
        return row[0] if row else None


    def get_chunks_by_call_id(self, call_id: str):
        query = """
        SELECT * FROM chunks
        WHERE call_id = ?
        ORDER BY sequence_id
        """
        return self.conn.execute(query, (call_id,)).fetchall()