from pydantic import BaseModel
from typing import List

class Chunk(BaseModel):
    chunk_id: str
    call_id: str
    text: str
    speaker: str
    timestamp: str
    sequence_id: int
    stage: str
    tags: List[str]