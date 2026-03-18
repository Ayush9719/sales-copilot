# Sales Copilot RAG System

## Overview

A CLI-based AI assistant to analyze sales call transcripts using
Retrieval-Augmented Generation (RAG).\
It ingests transcripts, performs semantic retrieval, reranks context,
and generates grounded answers with source attribution.

------------------------------------------------------------------------

## Features

-   Transcript ingestion & storage (SQLite + FAISS)
-   Hybrid retrieval (semantic + metadata)
-   LLM-based reranking
-   Context stitching
-   Grounded Q&A with sources
-   CLI interface
-   Basic test coverage

------------------------------------------------------------------------

## Architecture

Pipeline: 1. Retrieval (high recall) 2. Reranking (precision via LLM) 3.
Generation (grounded answers) 4. Source attribution

Components: - FAISS → vector search - SQLite → metadata - Ollama → LLM -
SentenceTransformers → embeddings

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

## Example Queries

-   What objections were raised?
-   Give me negative comments about pricing
-   Summarize the last call

------------------------------------------------------------------------

## Design Decisions

-   Separation of concerns (retrieval, reranking, generation)
-   LLM reranking for dynamic relevance
-   Context stitching for better reasoning
-   Source attribution handled outside LLM to prevent hallucination

------------------------------------------------------------------------

## Assumptions

-   File naming encodes metadata
-   Small dataset (optimized for clarity over scale)
-   Local LLM used (Ollama)

------------------------------------------------------------------------

## Future Improvements

-   Streaming responses
-   Cross-encoder reranking
-   Better intent parsing
-   Evaluation metrics

------------------------------------------------------------------------

## Tests

``` bash
PYTHONPATH=. uv run pytest
```

------------------------------------------------------------------------

## Github URL
https://github.com/Ayush9719/sales-copilot