# Sales Copilot – CLI RAG Assistant for Sales Calls

## Overview

This project is a command-line AI assistant for analyzing sales call transcripts.

It ingests transcript files, stores transcript chunks and embeddings, and answers natural-language questions over the calls using a Retrieval-Augmented Generation (RAG) pipeline. All responses include grounded source snippets so the user can see which conversation segments supported the answer.

This was built as a take-home assignment for a conversational AI copilot focused on sales call understanding and summarization.

---

## What It Supports

- Ingest sales call transcript files
- Store transcript chunks and metadata in SQLite
- Store vector embeddings for semantic retrieval in FAISS
- Answer natural-language questions over past calls
- Summarize the most recently ingested call
- List available call IDs
- Return source snippets with answers and summaries
- Basic automated tests for parsing, ingestion, and retrieval

---

## Example Commands

```bash
uv run python -m src.cli ingest-call data/1_demo_call.txt
uv run python -m src.cli query "What pricing concerns were raised?"
uv run python -m src.cli query "Give me all negative comments when pricing was mentioned in the calls"
uv run python -m src.cli query "summarize the last call"
uv run python -m src.cli query "list my call ids"
```
---

## Architecture

### High-level flow

1. Ingestion
 - Parse transcript lines into structured speaker turns
 - Chunk the transcript into searchable units
 - Extract metadata such as call_id, stage, speaker, and timestamp
 - Generate embeddings and persist the chunks

2. Retrieval
 - Convert the user query into an embedding
 - Retrieve semantically relevant transcript chunks from FAISS
 - Apply metadata-aware filtering where appropriate

3. Generation
 - Build a grounded prompt using retrieved transcript chunks
 - Use the LLM to generate a concise answer or call summary
 - Return the answer together with the supporting source snippets

---

## Storage Design

### SQLite

Used for structured transcript metadata and chunk storage.
Each chunk stores:
- chunk_id
- call_id 
- text
- speaker
- timestamp
- stage
- tags
- sequence_id

#### Why SQLite:
- simple local setup
- easy to inspect and debug 
- sufficient for a take-home sized dataset
- good fit for metadata filtering and ordered transcript retrieval

### FAISS

Used for vector similarity search over transcript chunk embeddings.

#### Why FAISS:
- lightweight and fast for local semantic retrieval
- easy to use for a small offline RAG system
- appropriate for local CLI-based experimentation

---

## Tech Stack
- Python
- SQLite for transcript metadata storage
- FAISS for vector retrieval
- SentenceTransformers for embeddings
- Ollama for local LLM inference
- Typer for the CLI
- Pytest for tests

---

## Setup

### 1. Install dependencies

``` bash
uv sync
```

### 2. Start Ollama

``` bash
ollama pull llama3
```

### 3. Run CLI

``` bash
uv run python -m src.cli
```

---

## Usage

### Ingest data

``` bash
uv run python -m src.cli ingest-call data/1_demo_call.txt
```

### Query

``` bash
uv run python -m src.cli query "What pricing concerns were raised?"
```

### List calls

``` bash
uv run python -m src.cli query "list my call ids"
```

### Summarize

``` bash
uv run python -m src.cli query "summarize the last call"
```

--- 

## Example Queries

- What pricing concerns were raised?
- What objections came up during the calls?
- Give me all negative comments when pricing was mentioned in the calls
- What did the customer ask for on security and legal terms?
- Summarize the last call

---

## Source Attribution

Every answer includes supporting source snippets.

Each source snippet shows:
 - call_id
 - timestamp
 - speaker  
 - supporting transcript text

This makes the output auditable and grounded in the original transcript content.

---

## Design Decisions

### Why SQLite + FAISS?

This assignment is small enough that a local, explicit design is more useful than introducing a heavier external database. SQLite keeps the metadata layer simple and inspectable, while FAISS handles semantic retrieval efficiently.

### Why a CLI?

The assignment explicitly asks for a simple command-line chatbot. A CLI keeps the project lightweight and easy to run in a review round.

### Why local Ollama?

Using a local LLM avoids external API dependencies and makes the project easier to run offline once dependencies are installed.

-   File naming encodes metadata
-   Small dataset (optimized for clarity over scale)
-   Local LLM used (Ollama)

---

## Assumptions

- Transcript files are plain text and follow a timestamped speaker-turn format like:
  - ```[00:21] Speaker: text```
- File names are used to derive call-level metadata such as call_id and stage
- ```summarize the last call``` refers to the most recently ingested call
- This implementation is optimized for a small local dataset and clarity of design rather than production scale

---

## Limitations

- Intent detection is rule-based and simple
- Retrieval is optimized for a small transcript set, not a large production corpus
- Transcript format handling is limited to the expected input style
- Local LLM output quality depends on the installed Ollama model

---

## Future Improvements

-   Streaming responses
-   Cross-encoder reranking
-   Better intent parsing
-   Evaluation metrics

---

## Tests

``` bash
PYTHONPATH=. uv run pytest
```

---

## Github URL
https://github.com/Ayush9719/sales-copilot