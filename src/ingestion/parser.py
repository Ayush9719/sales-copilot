import re
from typing import List, Dict

PATTERN = re.compile(r"\[(\d{2}:\d{2})\]\s*(.*?):\s*(.*)")

def parse_transcript(file_path: str) -> List[Dict]:
    results = []

    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        match = PATTERN.match(line)

        if match:
            timestamp, speaker, text = match.groups()

            results.append(
                {
                    "timestamp": timestamp,
                    "speaker": speaker.strip(),
                    "text": text.strip(),
                }
            )

    return results