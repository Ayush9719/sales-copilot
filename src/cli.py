import typer
from rich import print
from src.ingestion.pipeline import ingest
from src.ingestion.store_pipeline import store_chunks
from src.main import ask, summarize_call
from src.retrieval.query_intent import detect_intent
from src.storage.metadata_store import MetadataStore

app = typer.Typer()

@app.command()
def ingest_call(file_path: str):
    """
    Ingest a call transcript
    """
    chunks = ingest(file_path)
    store_chunks(chunks)

    print(f"[green]Ingested:[/green] {file_path}")

@app.command()
def query(q: str):
    intent = detect_intent(q)

    if intent == "list_calls":
        store = MetadataStore()
        calls = store.list_calls()

        print("\nAvailable Calls:\n")
        for c in calls:
            print(f"- {c}")

    elif intent == "summarize":
        summarize_call(q)

    elif intent == "negative_feedback":
        ask(q + " Focus on negative feedback and objections.")

    else:
        ask(q)

if __name__ == "__main__":
    app()