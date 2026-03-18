import os
from src.utils.constants import VALID_STAGES

def extract_metadata(file_path: str):
    filename = os.path.basename(file_path).lower()
    call_id = filename.replace(".txt", "")
    stage = "unknown"
    for s in VALID_STAGES:
        if s in filename:
            stage = s
            break
    return call_id, stage