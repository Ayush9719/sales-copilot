import re
from typing import List, Dict

TURN_RE = re.compile(r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*([^:]+):\s*(.*)$")

def strip_speaker_prefix(text: str, speaker: str) -> str:
    text = text.strip()
    speaker = speaker.strip()

    # remove exact repeated speaker prefix at the start
    pattern = rf"^{re.escape(speaker)}\s*:\s*"
    text = re.sub(pattern, "", text, count=1)

    return text.strip()


def parse_transcript(file_path: str) -> List[Dict]:
    results = []
    current = None

    with open(file_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")

            m = TURN_RE.match(line.strip())
            if m:
                if current:
                    results.append(current)

                timestamp, speaker, text = m.groups()
                speaker = speaker.strip()
                text = strip_speaker_prefix(text, speaker)

                current = {
                    "timestamp": timestamp.strip(),
                    "speaker": speaker,
                    "text": text,
                }
            else:
                if current and line.strip():
                    current["text"] += " " + line.strip()

    if current:
        results.append(current)

    return results