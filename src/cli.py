import typer
from rich import print
from src.ingestion.pipeline import ingest
from src.ingestion.store_pipeline import store_chunks
from src.main import ask
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
    """
    Ask a question about calls
    """
    ask(q)

@app.command()
def list_calls():
    store = MetadataStore()
    calls = store.list_calls()

    print("[bold]Available Calls:[/bold]")
    for c in calls:
        print(f"- {c}")

if __name__ == "__main__":
    app()